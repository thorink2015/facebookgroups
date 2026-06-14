"""
Seed the database with starter templates (and sample groups, if you have no
groups yet). Safe to run any time — it only fills in things that are empty,
it never overwrites or deletes your data.

    python seed.py
"""
import json
import os

import config
import db
from db import get_db, log_event
from util import canonicalize_group_url


def seed_templates():
    if not os.path.exists(config.TEMPLATES_JSON):
        print("  (no templates.json found, skipping template seed)")
        return
    with open(config.TEMPLATES_JSON, encoding="utf-8") as f:
        data = json.load(f)
    n_t = n_v = 0
    with get_db() as d:
        existing = d.execute("SELECT COUNT(*) c FROM templates").fetchone()["c"]
        if existing:
            print(f"  templates: {existing} already present, skipping.")
            return
        for t in data.get("templates", []):
            cur = d.execute(
                "INSERT INTO templates(code, name, audiences, image_types) "
                "VALUES (?, ?, ?, ?)",
                (t["code"], t.get("name", ""), t.get("audiences", ""),
                 t.get("image_types", "")))
            tid = cur.lastrowid
            n_t += 1
            for v in t.get("variants", []):
                d.execute("INSERT INTO variants(template_id, text) VALUES (?, ?)", (tid, v))
                n_v += 1
    # Log AFTER the transaction commits — never open a second connection while
    # the first one still holds a write lock (that's what caused a lock error).
    log_event(f"Seeded {n_t} templates / {n_v} variants.", "info")
    print(f"  templates: seeded {n_t} templates with {n_v} variants.")


def seed_sample_groups():
    sample = os.path.join(config.DATA_DIR, "sample_groups.csv")
    if not os.path.exists(sample):
        return
    with get_db() as d:
        existing = d.execute("SELECT COUNT(*) c FROM groups").fetchone()["c"]
        if existing:
            print(f"  groups: {existing} already present, skipping sample import.")
            return
    from util import parse_groups_csv
    with open(sample, "rb") as f:
        parsed = parse_groups_csv(f.read())
    added = 0
    with get_db() as d:
        for item in parsed:
            url, slug = canonicalize_group_url(item["url"])
            if not url:
                continue
            try:
                d.execute("INSERT INTO groups(url, name, category, fb_id, notes) "
                          "VALUES (?, ?, ?, ?, ?)",
                          (url, item.get("name", ""), item.get("category") or "uncategorized",
                           slug, item.get("notes", "")))
                added += 1
            except Exception:
                pass
    print(f"  groups: imported {added} sample groups (replace with your real CSV any time).")


if __name__ == "__main__":
    print("Seeding Tank Mix dashboard database...")
    db.init_db()
    seed_templates()
    seed_sample_groups()
    print("Done.")
