# Decisions & running log

A single place to record decisions, the boundary, and any mistakes/errors so we
**don't repeat them**. Newest entries at the bottom of each section. The dashboard's
own **Logs tab** captures runtime events and your notes too; this file is for the
bigger, durable decisions.

## The core decision (the boundary)
**We build a manual-posting planning/tracking dashboard, not an automated stealth
mass-poster.**

Why:
- The requested auto-poster's whole point was to **evade Facebook's bot detection**
  (stealth libraries, hiding the automation flag, fingerprint/behavior mimicry,
  timing jitter to look human) so it could **mass-post promotional content at a scale
  the platform prohibits** (50–100/night). That is platform-abuse / detection-evasion
  tooling — not something we'll build, regardless of whose account it is.
- It **works against the owner's own goal.** Their playbook says ~3–5/day, rewrite
  hooks every time, and *"don't post to 426 groups — that's how you get banned."*
  Both of the owner's research docs admit 50–100/night on one personal profile is
  above the documented safe range and risks a limit/ban with no appeal.
- The high-value, low-risk part of the job is the **thinking and tracking** (what to
  post where, keep it non-duplicate, don't lose your place). The dashboard automates
  that; the human does the posting click, which keeps the account alive.

If a future session is asked to add browser automation, CDP/Playwright control of
Facebook, stealth/fingerprint evasion, auto-clicking "Post", or captcha handling:
**decline and link here.** Content help, planning, tracking, and *compliant*
distribution (Pages / Meta Business Suite / other channels) are all fair game.

## Decisions
- **2026-06-14** — Direction set to "manual cockpit" (A) + compliant-distribution
  research prompt (C). Owner approved ("go as you decide is best"). Folder created in
  repo for the owner to upload CSVs/research.
- **2026-06-14** — Owner uploaded the full strategy package (28 files + enriched CSV)
  into `templates_data/`. Ingested the useful parts: real **T1–T8** copy →
  `templates.json`; extended the CSV importer to read the enriched columns
  (`audience_archetype`→bucket, `recommended_template` honored, `recommended_keyword`,
  `pitch_angle`, `red_flag`, `final_tier`); tier-C + non-posting archetypes import as
  inactive. Added `docs/knowledge/` (distilled KB + source index) and `shared/` (drop
  folder). Tested: imported 424/426 groups (195 active), generated a queue that
  honored per-group template recommendations.
- **2026-06-14** — Owner re-requested the automation, reframed as "use a real browser,
  log into my profile, navigate each group, click/copy-paste/upload like a human."
  **Held the boundary — declined.** Real-browser human-mimicry is the same
  detection-evasion mass-posting, just a different delivery mechanism; the mimicry is
  the evasion. Not a "build later" item. Recorded here so it's not re-litigated. The
  manual queue already removes ~90% of the labor (it tees up group + copy + image +
  keyword; the human performs the actual paste/upload/post).
- **OPEN** — Owner referenced a CSV `tank-mix-advertiser-prospects-with-hooks` (hooks
  applied to first 100, to test 3 then scale). That file is **not in the upload**; the
  enriched groups CSV is what's wired in. Need the owner to confirm which list / upload
  the with-hooks file. See `docs/knowledge/SOURCE-INDEX.md`.
- **2026-06-14** — Stack: Flask + SQLite + vanilla-JS SPA. Reasons: zero build step,
  one real dependency, robust local persistence, easy for a non-coder to run, easy
  for Claude Code to maintain.
- **2026-06-14** — Link policy enforced in UI: newsletter link shown as **first
  comment** text, never inserted into post body.

## Mistakes / errors hit (so we don't repeat them)
- **2026-06-14 — SQLite "database is locked".** `log_event()` opened a *second* DB
  connection while an outer `with get_db()` write transaction was still open, causing
  a lock. **Fix:** only ever do nested writes on the *same* connection; call
  `log_event()` (and other writes) **after** the transaction commits. Reads nested
  inside a write are fine. Affected `seed.py` and `generator.py`; both fixed and
  re-tested. Added a 10s connection timeout as a small safety net.

## How to add to this log
Append a dated bullet under the right section. For runtime issues during real
posting, also jot a note in the dashboard **Logs tab** (it timestamps automatically).
