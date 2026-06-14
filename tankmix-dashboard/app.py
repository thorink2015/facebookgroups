"""
Tank Mix Campaign Dashboard — local web app.

WHAT THIS IS
  A planning + tracking cockpit for promoting the Tank Mix newsletter in
  Facebook groups, by hand, at a safe cadence. It organizes your copy and
  images, builds a "do this next" queue of non-duplicate posts, and logs
  every post so you never repeat yourself or lose track.

WHAT THIS IS NOT
  It does NOT log into Facebook, drive a browser, or post for you. You do the
  actual posting (a few clicks per group). That keeps your real account safe
  and keeps you inside your own posting playbook.

RUN IT
  See README.md. Short version:  python app.py   then open http://127.0.0.1:5000
"""
import csv
import io
import os

from flask import (
    Flask, jsonify, request, send_from_directory, Response, abort,
)
from werkzeug.utils import secure_filename

import config
import db
from db import get_db, get_settings, set_setting, log_event
from generator import generate_queue
from util import canonicalize_group_url, parse_groups_csv

app = Flask(__name__, static_folder=config.STATIC_DIR, static_url_path="/static")
db.init_db()


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def row(r):
    return dict(r) if r is not None else None


def rows(rs):
    return [dict(r) for r in rs]


# --------------------------------------------------------------------------- #
# Pages + static assets
# --------------------------------------------------------------------------- #
@app.route("/")
def index():
    return send_from_directory(config.STATIC_DIR, "index.html")


@app.route("/images/<path:filename>")
def serve_image(filename):
    return send_from_directory(config.IMAGES_DIR, filename)


@app.route("/api/health")
def health():
    return jsonify({"ok": True})


# --------------------------------------------------------------------------- #
# Overview / stats
# --------------------------------------------------------------------------- #
@app.route("/api/overview")
def overview():
    with get_db() as d:
        def scalar(q, args=()):
            v = d.execute(q, args).fetchone()
            return list(v)[0] if v else 0

        posts_today = scalar(
            "SELECT COUNT(*) FROM posts WHERE status='posted' "
            "AND date(posted_at)=date('now','localtime')")
        posts_week = scalar(
            "SELECT COUNT(*) FROM posts WHERE status='posted' "
            "AND posted_at >= datetime('now','-7 days')")
        posts_total = scalar("SELECT COUNT(*) FROM posts WHERE status='posted'")
        planned = scalar("SELECT COUNT(*) FROM posts WHERE status='planned'")
        groups_total = scalar("SELECT COUNT(*) FROM groups WHERE active=1")
        groups_covered = scalar(
            "SELECT COUNT(DISTINCT group_id) FROM posts WHERE status='posted'")
        last_activity = scalar("SELECT MAX(posted_at) FROM posts WHERE status='posted'")
        templates_n = scalar("SELECT COUNT(*) FROM templates WHERE active=1")
        variants_n = scalar("SELECT COUNT(*) FROM variants WHERE active=1")
        images_n = scalar("SELECT COUNT(*) FROM images WHERE active=1")

        recent = rows(d.execute(
            """SELECT p.id, p.status, p.post_url, p.posted_at,
                      g.name AS group_name, g.url AS group_url, g.category,
                      t.code AS template_code
               FROM posts p
               LEFT JOIN groups g ON g.id=p.group_id
               LEFT JOIN templates t ON t.id=p.template_id
               WHERE p.status IN ('posted','skipped','failed')
               ORDER BY COALESCE(p.posted_at, p.generated_at) DESC
               LIMIT 12""").fetchall())

        by_category = rows(d.execute(
            """SELECT category,
                      COUNT(*) AS total,
                      SUM(CASE WHEN id IN
                          (SELECT group_id FROM posts WHERE status='posted')
                          THEN 1 ELSE 0 END) AS covered
               FROM groups WHERE active=1
               GROUP BY category ORDER BY total DESC""").fetchall())

    settings = get_settings()
    daily_cap = int(settings.get("daily_cap", "10"))
    high_warn = int(settings.get("high_volume_warn", "15"))
    status = "idle"
    if planned > 0:
        status = "queue_ready"
    if posts_today >= high_warn:
        cadence = "high"
    elif posts_today >= daily_cap:
        cadence = "at_cap"
    else:
        cadence = "ok"

    return jsonify({
        "status": status,
        "cadence": cadence,
        "posts_today": posts_today,
        "posts_week": posts_week,
        "posts_total": posts_total,
        "planned": planned,
        "groups_total": groups_total,
        "groups_covered": groups_covered,
        "groups_remaining": max(0, groups_total - groups_covered),
        "last_activity": last_activity,
        "templates": templates_n,
        "variants": variants_n,
        "images": images_n,
        "daily_cap": daily_cap,
        "high_volume_warn": high_warn,
        "recent": recent,
        "by_category": by_category,
        "settings": settings,
    })


# --------------------------------------------------------------------------- #
# Settings
# --------------------------------------------------------------------------- #
@app.route("/api/settings", methods=["GET", "POST"])
def settings_api():
    if request.method == "POST":
        data = request.get_json(force=True) or {}
        for k, v in data.items():
            set_setting(k, v)
        log_event("Settings updated.", "info")
    return jsonify(get_settings())


# --------------------------------------------------------------------------- #
# Groups
# --------------------------------------------------------------------------- #
@app.route("/api/groups", methods=["GET"])
def list_groups():
    q = (request.args.get("q") or "").strip().lower()
    category = (request.args.get("category") or "").strip()
    with get_db() as d:
        gs = rows(d.execute(
            """SELECT g.*,
                      (SELECT MAX(posted_at) FROM posts p
                        WHERE p.group_id=g.id AND p.status='posted') AS last_posted,
                      (SELECT COUNT(*) FROM posts p
                        WHERE p.group_id=g.id AND p.status='posted') AS post_count
               FROM groups g ORDER BY g.category, g.name""").fetchall())
    if q:
        gs = [g for g in gs if q in (g["name"] or "").lower()
              or q in (g["url"] or "").lower() or q in (g["category"] or "").lower()]
    if category:
        gs = [g for g in gs if (g["category"] or "") == category]
    return jsonify(gs)


@app.route("/api/groups", methods=["POST"])
def add_group():
    data = request.get_json(force=True) or {}
    url, slug = canonicalize_group_url(data.get("url", ""))
    if not url:
        return jsonify({"error": "A group URL is required."}), 400
    with get_db() as d:
        try:
            d.execute(
                "INSERT INTO groups(url, name, category, fb_id, notes) "
                "VALUES (?, ?, ?, ?, ?)",
                (url, data.get("name", ""),
                 data.get("category", "uncategorized") or "uncategorized",
                 slug, data.get("notes", "")))
        except Exception:
            return jsonify({"error": "That group is already in the list."}), 409
    return jsonify({"ok": True})


@app.route("/api/groups/<int:gid>", methods=["PATCH", "DELETE"])
def edit_group(gid):
    if request.method == "DELETE":
        with get_db() as d:
            d.execute("DELETE FROM groups WHERE id=?", (gid,))
        return jsonify({"ok": True})
    data = request.get_json(force=True) or {}
    fields, vals = [], []
    for key in ("name", "category", "notes", "active"):
        if key in data:
            fields.append(f"{key}=?")
            vals.append(data[key])
    if data.get("url"):
        url, slug = canonicalize_group_url(data["url"])
        fields += ["url=?", "fb_id=?"]
        vals += [url, slug]
    if fields:
        vals.append(gid)
        with get_db() as d:
            d.execute(f"UPDATE groups SET {', '.join(fields)} WHERE id=?", vals)
    return jsonify({"ok": True})


@app.route("/api/groups/import", methods=["POST"])
def import_groups():
    """Upload a CSV of groups. Dedupes by canonical URL. Never deletes."""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded."}), 400
    data = request.files["file"].read()
    parsed = parse_groups_csv(data)
    added = skipped = 0
    with get_db() as d:
        for item in parsed:
            url, slug = canonicalize_group_url(item["url"])
            if not url:
                skipped += 1
                continue
            try:
                d.execute(
                    "INSERT INTO groups(url, name, category, fb_id, notes) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (url, item.get("name", ""), item.get("category") or "uncategorized",
                     slug, item.get("notes", "")))
                added += 1
            except Exception:
                skipped += 1  # already present
    log_event(f"CSV import: {added} added, {skipped} skipped (duplicates/blank).", "info")
    return jsonify({"added": added, "skipped": skipped, "parsed": len(parsed)})


# --------------------------------------------------------------------------- #
# Templates + variants
# --------------------------------------------------------------------------- #
@app.route("/api/templates", methods=["GET"])
def list_templates():
    with get_db() as d:
        ts = rows(d.execute("SELECT * FROM templates ORDER BY code").fetchall())
        for t in ts:
            t["variants"] = rows(d.execute(
                "SELECT * FROM variants WHERE template_id=? ORDER BY id", (t["id"],)
            ).fetchall())
    return jsonify(ts)


@app.route("/api/templates", methods=["POST"])
def add_template():
    data = request.get_json(force=True) or {}
    code = (data.get("code") or "").strip()
    if not code:
        return jsonify({"error": "A template code (e.g. T1) is required."}), 400
    with get_db() as d:
        try:
            cur = d.execute(
                "INSERT INTO templates(code, name, audiences, image_types) "
                "VALUES (?, ?, ?, ?)",
                (code, data.get("name", ""), data.get("audiences", ""),
                 data.get("image_types", "")))
            tid = cur.lastrowid
        except Exception:
            return jsonify({"error": "A template with that code already exists."}), 409
    return jsonify({"ok": True, "id": tid})


@app.route("/api/templates/<int:tid>", methods=["PATCH", "DELETE"])
def edit_template(tid):
    if request.method == "DELETE":
        with get_db() as d:
            d.execute("DELETE FROM templates WHERE id=?", (tid,))
        return jsonify({"ok": True})
    data = request.get_json(force=True) or {}
    fields, vals = [], []
    for key in ("code", "name", "audiences", "image_types", "active"):
        if key in data:
            fields.append(f"{key}=?")
            vals.append(data[key])
    if fields:
        vals.append(tid)
        with get_db() as d:
            d.execute(f"UPDATE templates SET {', '.join(fields)} WHERE id=?", vals)
    return jsonify({"ok": True})


@app.route("/api/templates/<int:tid>/variants", methods=["POST"])
def add_variant(tid):
    data = request.get_json(force=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "Variant text is required."}), 400
    with get_db() as d:
        d.execute("INSERT INTO variants(template_id, text) VALUES (?, ?)", (tid, text))
    return jsonify({"ok": True})


@app.route("/api/variants/<int:vid>", methods=["PATCH", "DELETE"])
def edit_variant(vid):
    if request.method == "DELETE":
        with get_db() as d:
            d.execute("DELETE FROM variants WHERE id=?", (vid,))
        return jsonify({"ok": True})
    data = request.get_json(force=True) or {}
    fields, vals = [], []
    for key in ("text", "active"):
        if key in data:
            fields.append(f"{key}=?")
            vals.append(data[key])
    if fields:
        vals.append(vid)
        with get_db() as d:
            d.execute(f"UPDATE variants SET {', '.join(fields)} WHERE id=?", vals)
    return jsonify({"ok": True})


# --------------------------------------------------------------------------- #
# Images
# --------------------------------------------------------------------------- #
@app.route("/api/images", methods=["GET"])
def list_images():
    with get_db() as d:
        return jsonify(rows(d.execute(
            "SELECT * FROM images ORDER BY uploaded_at DESC").fetchall()))


@app.route("/api/images", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded."}), 400
    f = request.files["file"]
    name = secure_filename(f.filename or "")
    ext = os.path.splitext(name)[1].lower()
    if ext not in config.ALLOWED_IMAGE_EXT:
        return jsonify({"error": f"Unsupported file type {ext}. "
                        f"Allowed: {', '.join(sorted(config.ALLOWED_IMAGE_EXT))}"}), 400
    # Avoid collisions.
    dest = os.path.join(config.IMAGES_DIR, name)
    base, e = os.path.splitext(name)
    i = 1
    while os.path.exists(dest):
        name = f"{base}_{i}{e}"
        dest = os.path.join(config.IMAGES_DIR, name)
        i += 1
    f.save(dest)
    image_type = (request.form.get("image_type") or "hero").strip()
    caption = (request.form.get("caption") or "").strip()
    with get_db() as d:
        d.execute("INSERT INTO images(filename, image_type, caption) VALUES (?, ?, ?)",
                  (name, image_type, caption))
    log_event(f"Image uploaded: {name} ({image_type}).", "info")
    return jsonify({"ok": True, "filename": name})


@app.route("/api/images/<int:iid>", methods=["PATCH", "DELETE"])
def edit_image(iid):
    with get_db() as d:
        img = d.execute("SELECT * FROM images WHERE id=?", (iid,)).fetchone()
        if not img:
            return jsonify({"error": "Not found."}), 404
        if request.method == "DELETE":
            d.execute("DELETE FROM images WHERE id=?", (iid,))
            try:
                os.remove(os.path.join(config.IMAGES_DIR, img["filename"]))
            except OSError:
                pass
            return jsonify({"ok": True})
        data = request.get_json(force=True) or {}
        fields, vals = [], []
        for key in ("image_type", "caption", "active"):
            if key in data:
                fields.append(f"{key}=?")
                vals.append(data[key])
        if fields:
            vals.append(iid)
            d.execute(f"UPDATE images SET {', '.join(fields)} WHERE id=?", vals)
    return jsonify({"ok": True})


# --------------------------------------------------------------------------- #
# Queue (planned posts) + actions
# --------------------------------------------------------------------------- #
def _queue_rows(d, status_filter):
    return rows(d.execute(
        f"""SELECT p.*,
                   g.name AS group_name, g.url AS group_url, g.category,
                   t.code AS template_code, t.name AS template_name,
                   i.filename AS image_filename, i.image_type AS image_type,
                   i.caption AS image_caption
            FROM posts p
            LEFT JOIN groups g ON g.id=p.group_id
            LEFT JOIN templates t ON t.id=p.template_id
            LEFT JOIN images i ON i.id=p.image_id
            WHERE p.status {status_filter}
            ORDER BY p.id""").fetchall())


@app.route("/api/queue")
def get_queue():
    with get_db() as d:
        return jsonify(_queue_rows(d, "= 'planned'"))


@app.route("/api/queue/generate", methods=["POST"])
def queue_generate():
    data = request.get_json(silent=True) or {}
    count = data.get("count")
    result = generate_queue(count)
    return jsonify(result)


@app.route("/api/queue/clear", methods=["POST"])
def queue_clear():
    with get_db() as d:
        d.execute("DELETE FROM posts WHERE status='planned'")
    log_event("Cleared the planned queue.", "info")
    return jsonify({"ok": True})


@app.route("/api/posts/<int:pid>/status", methods=["POST"])
def set_post_status(pid):
    """Mark a queue item posted / skipped / failed. Updates rotation counters."""
    data = request.get_json(force=True) or {}
    status = data.get("status", "posted")
    if status not in ("posted", "skipped", "failed", "planned"):
        return jsonify({"error": "Bad status."}), 400
    with get_db() as d:
        post = d.execute("SELECT * FROM posts WHERE id=?", (pid,)).fetchone()
        if not post:
            return jsonify({"error": "Not found."}), 404
        d.execute(
            """UPDATE posts SET status=?, post_url=?, link_in_comment=?, notes=?,
                                posted_at=CASE WHEN ?='posted'
                                          THEN datetime('now','localtime') ELSE posted_at END
               WHERE id=?""",
            (status, data.get("post_url", post["post_url"]),
             1 if data.get("link_in_comment") else 0,
             data.get("notes", post["notes"]), status, pid))
        if status == "posted":
            if post["variant_id"]:
                d.execute("UPDATE variants SET times_used=times_used+1, "
                          "last_used_at=datetime('now') WHERE id=?", (post["variant_id"],))
            if post["image_id"]:
                d.execute("UPDATE images SET times_used=times_used+1, "
                          "last_used_at=datetime('now') WHERE id=?", (post["image_id"],))
    return jsonify({"ok": True})


@app.route("/api/posts/<int:pid>/regenerate", methods=["POST"])
def regenerate_post(pid):
    """Re-pick the variant and image for a single planned item."""
    from generator import _pick_variant, _pick_image, _recent_used_ids
    with get_db() as d:
        post = d.execute("SELECT * FROM posts WHERE id=?", (pid,)).fetchone()
        if not post or post["status"] != "planned":
            return jsonify({"error": "Only planned items can be regenerated."}), 400
        settings = get_settings()
        dup_days = int(settings.get("dup_window_days", "14"))
        recent_v = _recent_used_ids(d, "variant_id", "posts", dup_days)
        recent_i = _recent_used_ids(d, "image_id", "posts", dup_days)
        tmpl = d.execute("SELECT * FROM templates WHERE id=?", (post["template_id"],)).fetchone()
        avoid_v = {post["variant_id"]} if post["variant_id"] else set()
        avoid_i = {post["image_id"]} if post["image_id"] else set()
        variant = _pick_variant(d, post["template_id"], avoid_v, recent_v)
        image = _pick_image(d, tmpl["image_types"] if tmpl else "", avoid_i, recent_i)
        d.execute("UPDATE posts SET variant_id=?, image_id=?, copy_text=? WHERE id=?",
                  (variant["id"] if variant else post["variant_id"],
                   image["id"] if image else post["image_id"],
                   variant["text"] if variant else post["copy_text"], pid))
    return jsonify({"ok": True})


@app.route("/api/posts/<int:pid>", methods=["PATCH", "DELETE"])
def edit_post(pid):
    if request.method == "DELETE":
        with get_db() as d:
            d.execute("DELETE FROM posts WHERE id=?", (pid,))
        return jsonify({"ok": True})
    data = request.get_json(force=True) or {}
    with get_db() as d:
        if "copy_text" in data:
            d.execute("UPDATE posts SET copy_text=? WHERE id=?", (data["copy_text"], pid))
    return jsonify({"ok": True})


# --------------------------------------------------------------------------- #
# History + logs
# --------------------------------------------------------------------------- #
@app.route("/api/history")
def history():
    with get_db() as d:
        return jsonify(_queue_rows(d, "IN ('posted','skipped','failed')"))


@app.route("/api/history/export.csv")
def export_history():
    with get_db() as d:
        data = _queue_rows(d, "IN ('posted','skipped','failed')")
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["id", "status", "group_name", "group_url", "category",
                "template_code", "image_filename", "post_url",
                "link_in_comment", "posted_at", "copy_text", "notes"])
    for p in data:
        w.writerow([p["id"], p["status"], p.get("group_name"), p.get("group_url"),
                    p.get("category"), p.get("template_code"), p.get("image_filename"),
                    p.get("post_url"), p.get("link_in_comment"), p.get("posted_at"),
                    (p.get("copy_text") or "").replace("\n", " "), p.get("notes")])
    return Response(buf.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=tankmix_history.csv"})


@app.route("/api/logs", methods=["GET", "POST"])
def logs_api():
    if request.method == "POST":
        data = request.get_json(force=True) or {}
        log_event(data.get("message", ""), data.get("level", "info"))
        return jsonify({"ok": True})
    with get_db() as d:
        return jsonify(rows(d.execute(
            "SELECT * FROM event_log ORDER BY id DESC LIMIT 200").fetchall()))


if __name__ == "__main__":
    print("\n  Tank Mix Campaign Dashboard")
    print(f"  Open  ->  http://{config.HOST}:{config.PORT}\n")
    app.run(host=config.HOST, port=config.PORT, debug=False)
