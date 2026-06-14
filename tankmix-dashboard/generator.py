"""
The brain of the dashboard: build a session "queue" of posts to make by hand.

It does NOT post anything. It just decides, for each chosen group:
  - which template to use (matched to the group's category),
  - which copy variant (rotated so you never repeat the same words too soon),
  - which image (matched to the template's image types, least-recently-used).

The result is a set of rows in the `posts` table with status='planned' that
show up in the Daily Queue tab. You then post each one yourself.
"""
import random

from db import get_db, get_settings, log_event


def _recent_used_ids(db, column, table, days):
    """IDs of variants/images used (planned or posted) within the last N days."""
    rows = db.execute(
        f"""SELECT DISTINCT {column} AS id FROM posts
            WHERE {column} IS NOT NULL
              AND status IN ('planned','posted')
              AND COALESCE(posted_at, generated_at) >= datetime('now', ?)""",
        (f"-{int(days)} days",),
    ).fetchall()
    return {r["id"] for r in rows}


def _eligible_groups(db, cooldown_days):
    """
    Groups that are active, not already in the current planned queue, and not
    posted to within the cooldown window. Ordered least-recently-posted first.
    """
    rows = db.execute(
        """
        SELECT g.*,
               (SELECT MAX(posted_at) FROM posts p
                 WHERE p.group_id = g.id AND p.status='posted') AS last_posted,
               (SELECT COUNT(*) FROM posts p
                 WHERE p.group_id = g.id AND p.status='planned') AS planned_count
        FROM groups g
        WHERE g.active = 1
        """
    ).fetchall()

    eligible = []
    for r in rows:
        if r["planned_count"] and r["planned_count"] > 0:
            continue  # already queued, don't double up
        if r["last_posted"]:
            cd = db.execute(
                "SELECT (julianday('now') - julianday(?)) AS d", (r["last_posted"],)
            ).fetchone()["d"]
            if cd is not None and cd < float(cooldown_days):
                continue
        eligible.append(r)

    # Least-recently-posted first; never-posted (NULL) come first. Light shuffle
    # within equal buckets so it doesn't feel mechanical.
    random.shuffle(eligible)
    eligible.sort(key=lambda r: (r["last_posted"] or ""))
    return eligible


def _pick_template(db, group):
    """Pick a template for a group. Honor the CSV's recommended_template first;
    otherwise match an active template whose audiences include the group's
    category; otherwise fall back to any active template."""
    templates = db.execute("SELECT * FROM templates WHERE active = 1").fetchall()
    if not templates:
        return None
    # 1. Research-recommended template for this specific group.
    rec = (group["rec_template"] or "").strip().upper() if "rec_template" in group.keys() else ""
    if rec:
        for t in templates:
            if (t["code"] or "").strip().upper() == rec:
                return t
    # 2. Audience-bucket match.
    cat = (group["category"] or "").strip().lower()
    matching = [
        t for t in templates
        if cat and cat in [a.strip().lower() for a in (t["audiences"] or "").split(",") if a.strip()]
    ]
    pool = matching or templates
    return random.choice(pool)


def _pick_variant(db, template_id, avoid_ids, recent_ids):
    rows = db.execute(
        "SELECT * FROM variants WHERE template_id = ? AND active = 1",
        (template_id,),
    ).fetchall()
    if not rows:
        return None
    fresh = [v for v in rows if v["id"] not in avoid_ids and v["id"] not in recent_ids]
    pool = fresh or [v for v in rows if v["id"] not in avoid_ids] or rows
    # Prefer the least used / least recently used inside the chosen pool.
    pool.sort(key=lambda v: (v["times_used"] or 0, v["last_used_at"] or ""))
    return pool[0]


def _pick_image(db, image_types, avoid_ids, recent_ids):
    types = [t.strip().lower() for t in (image_types or "").split(",") if t.strip()]
    rows = db.execute("SELECT * FROM images WHERE active = 1").fetchall()
    if not rows:
        return None
    typed = [im for im in rows if (im["image_type"] or "").lower() in types] if types else rows
    candidates = typed or rows
    fresh = [im for im in candidates if im["id"] not in avoid_ids and im["id"] not in recent_ids]
    pool = fresh or [im for im in candidates if im["id"] not in avoid_ids] or candidates
    pool.sort(key=lambda im: (im["times_used"] or 0, im["last_used_at"] or ""))
    return pool[0]


def generate_queue(count=None):
    """
    Create up to `count` planned posts. Returns a summary dict.
    """
    settings = get_settings()
    if count is None:
        count = int(settings.get("session_target", "5"))
    count = max(1, int(count))
    dup_days = int(settings.get("dup_window_days", "14"))
    cooldown = int(settings.get("group_cooldown_days", "7"))

    created = 0
    warnings = []
    no_groups = False
    with get_db() as db:
        groups = _eligible_groups(db, cooldown)
        if not groups:
            no_groups = True
            groups = []

        recent_variants = _recent_used_ids(db, "variant_id", "posts", dup_days)
        recent_images = _recent_used_ids(db, "image_id", "posts", dup_days)
        used_variants_tonight = set()
        used_images_tonight = set()

        for g in groups:
            if created >= count:
                break
            template = _pick_template(db, g)
            if not template:
                warnings.append("No active templates exist. Add at least one template + variant.")
                break

            variant = _pick_variant(
                db, template["id"], used_variants_tonight, recent_variants
            )
            if not variant:
                # This template has no usable variant; try another group/template.
                warnings.append(f"Template {template['code']} has no active variant; skipped a group.")
                continue

            image = _pick_image(
                db, template["image_types"], used_images_tonight, recent_images
            )
            # image may be None if no images uploaded yet — that's allowed, the
            # queue item just won't have a suggested image.

            copy_text = variant["text"]

            db.execute(
                """INSERT INTO posts
                   (group_id, template_id, variant_id, image_id, copy_text, status)
                   VALUES (?, ?, ?, ?, ?, 'planned')""",
                (g["id"], template["id"], variant["id"],
                 image["id"] if image else None, copy_text),
            )
            used_variants_tonight.add(variant["id"])
            if image:
                used_images_tonight.add(image["id"])
            created += 1

    # Logging happens AFTER the write transaction above has committed.
    if no_groups:
        log_event("Generate: no eligible groups (all on cooldown or none imported).", "warn")
        return {"created": 0, "warnings": ["No eligible groups right now. "
                "Either import groups, or wait out the per-group cooldown."]}

    log_event(f"Generated {created} planned post(s).", "info")
    if created == 0 and not warnings:
        warnings.append("Nothing was generated. Check that you have groups, templates and variants.")
    return {"created": created, "warnings": warnings}
