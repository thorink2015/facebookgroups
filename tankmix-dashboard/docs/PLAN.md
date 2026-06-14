# Build plan (batches)

Big task, built in batches. This is the live checklist.

## ✅ Batch 1 — Dashboard core (DONE)
- Folder structure + git scaffolding.
- SQLite schema: groups, templates, variants, images, posts, settings, event_log.
- Flask API: overview, settings, groups (+CSV import), templates+variants, images
  (+upload), queue (generate/clear), post status/regenerate, history (+CSV export), logs.
- Non-duplicate **queue generator** (template↔category matching, variant + image
  rotation, dedupe window, per-group cooldown).
- SPA dashboard (Overview, Daily Queue, Groups, Templates, Images, History,
  Settings, Logs) with copy-to-clipboard, image preview, first-comment helper,
  mark-posted, regenerate.
- One-command start scripts (`start.sh` / `start.bat`), seed data, READMEs, memory.
- **Smoke-tested end to end** (seed → generate → mark posted → history → export).

## ⏳ Batch 2 — Your content + your data (needs YOU)
What I need from you (drop into the repo or the dashboard):
1. **Your real groups CSV** → import in the Groups tab. Add a `category` column if
   you can (`operators`, `farmer_operators`, `drone_curious`, `specialty`) so copy
   gets matched well. Without it everything still works, just less targeted.
2. **Your 4–5 images** → upload in the Images tab, tagged by type.
3. **Your real T1–T8 copy + hook variants** → replace the starter text in Templates.
4. **Your newsletter link** → Settings tab.
5. Optional: upload your raw research/playbook docs to `docs/research/` for the record.

## ⏳ Batch 3 — Polish after first real use (after you try it)
Likely candidates once you've run a real session:
- Light auto-spinning of hooks (synonym/emoji variation) if you want even more variety.
- A "shadow-ban check" reminder list (re-open a sample of posts to confirm they're live).
- Per-category cadence rules, scheduling reminders, simple charts.
- Optional Claude-assisted hook rewriting (you paste, it rewrites) — kept manual/cheap.

## ⏳ Batch 4 (optional) — Compliant scaled distribution
If you want true "set it and walk away," the supported path is a Facebook **Page**
and/or a group **you admin**, scheduled via **Meta Business Suite**. See
`compliant-distribution-research-prompt.md` to research it properly first.
