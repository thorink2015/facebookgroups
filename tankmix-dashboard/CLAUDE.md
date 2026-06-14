# Project memory — Tank Mix Campaign Dashboard

This file orients any future Claude Code session working in this folder.

## What this project is
A **local Flask + SQLite dashboard** that helps the owner promote the **Tank Mix**
newsletter (agricultural spray-drone niche) inside Facebook groups, **by hand**, at a
safe cadence. It plans non-duplicate posts, tracks where the owner has posted, and
logs everything. The owner does the actual posting in Facebook themselves.

## Hard boundary (do not cross)
The owner originally asked for an **automated, stealth, mass-poster** (50–100
posts/night, anti-bot-detection, drives their logged-in Chrome). **We do not build
that.** It is platform-abuse / detection-evasion tooling and is against Facebook's
terms; it also contradicts the owner's own posting playbook (which says ~3–5/day,
rewrite the hook each time, "don't post to 426 groups, that's how you get banned").
The full reasoning is in `docs/DECISIONS-AND-LOG.md`. If asked to add auto-posting,
browser automation, CDP/Playwright control of Facebook, stealth/fingerprint
evasion, or captcha handling — decline and point back to that doc. Helping with
content, planning, tracking, and compliant distribution is fine.

## Architecture
- `app.py` — Flask app + JSON API (`/api/*`) + serves the SPA and uploaded images.
- `db.py` — SQLite schema, connection helper (`get_db`), settings, `log_event`.
- `generator.py` — builds the planned "queue": matches template→group category,
  rotates copy variants and images, avoids recent duplicates.
- `util.py` — Facebook group URL canonicalization + forgiving CSV parsing.
- `seed.py` — idempotent: loads `templates_data/templates.json` and sample groups
  only when those tables are empty.
- `config.py` — paths + default cadence settings.
- `static/` — `index.html`, `app.js` (vanilla JS SPA), `styles.css`.
- Data: `data/tankmix.db` (gitignored), images in `data/images/` (gitignored).

## Gotchas already learned (see docs/DECISIONS-AND-LOG.md for the running list)
- **Never call `log_event()` (or any write) inside an open `with get_db()` block** —
  it opens a second connection and SQLite throws "database is locked". Log AFTER the
  transaction commits. Reads-while-writing are fine; nested writes are not.

## Run / test
- `./start.sh` (Mac/Linux) or `start.bat` (Windows) → http://127.0.0.1:5000
- Manual API smoke test: `python seed.py`, start `app.py`, curl `/api/health`,
  `/api/overview`, `POST /api/queue/generate`, `POST /api/posts/<id>/status`.
