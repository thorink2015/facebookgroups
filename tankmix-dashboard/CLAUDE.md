# Project memory — Tank Mix Campaign Dashboard

This file orients any future Claude Code session working in this folder.

## What this project is
A **local Flask + SQLite dashboard** that helps the owner promote the **Tank Mix**
newsletter (agricultural spray-drone niche) inside Facebook groups, **by hand**, at a
safe cadence. It plans non-duplicate posts, tracks where the owner has posted, and
logs everything. The owner does the actual posting in Facebook themselves.

## Hard boundary (do not cross)
The owner has asked (more than once, incl. a "drive a real browser and mimic a human
clicking" framing) for an **automated, stealth, mass-poster** (50–100 posts/night,
anti-bot-detection, drives their logged-in Chrome). **We do not build that** — in any
framing. Headless script vs. real-browser-mimicking-a-human is the same thing: the
human-mimicry IS the detection evasion. It's platform abuse, against Facebook's terms,
and contradicts the owner's own playbook (~3–5/day, rewrite the hook each time,
"don't post to 426 groups, that's how you get banned"). Full reasoning in
`docs/DECISIONS-AND-LOG.md`. If asked to add auto-posting, browser automation,
CDP/Playwright/Selenium control of Facebook, human-input simulation, stealth/
fingerprint evasion, or captcha handling — decline and point back to that doc.
Helping with content, planning, tracking, and compliant distribution is fine.

## Content & data (what's been ingested)
- The owner uploaded a full strategy package into `templates_data/` (28 files +
  the enriched CSV). It's indexed in `docs/knowledge/SOURCE-INDEX.md` and distilled
  in `docs/knowledge/KNOWLEDGE-BASE.md` — **read those two first** for context.
- Real **T1–T8** copy is in `templates_data/templates.json` (with per-template keyword).
- The CSV to import is `templates_data/01-data/01-fb-groups-enriched.csv` (426 groups;
  the importer maps `audience_archetype`→bucket and honors `recommended_template`).
- `shared/` is the owner's go-forward drop folder for files to share with us.

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
