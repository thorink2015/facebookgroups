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
