# Source index — where everything lives

You uploaded a full strategy package into `tankmix-dashboard/templates_data/`. This
maps what each file is so I can jump straight to the right one. (`KNOWLEDGE-BASE.md`
is the distilled version of all of it.)

## The package (under `templates_data/`)
| File | What it is | Pulled into the app? |
|---|---|---|
| `00-README-master-index.md` | Master index of the whole package | reference |
| `01-data/01-fb-groups-enriched.csv` | **426 groups + 8 research columns** (tier, archetype, rec template, keyword, pitch, red flag) | ✅ this is the CSV to import in the Groups tab |
| `02-research/01-research-master-consolidated.md` | All 6 research batches | reference for copy optimization |
| `03-execution/01-facebook-posting-playbook.md` | **The 8 templates + cadence + rules** | ✅ T1–T8 copy now in `templates_data/templates.json` |
| `03-execution/02-top-50-groups-mapped.md` | A1–A50 priority list with URLs | reference |
| `03-execution/03-personal-profile-setup.md` | Bio/photo/cover/pinned-post specs | do once, by hand |
| `03-execution/04-keyword-optin-mechanic.md` | 9 keywords + DM templates + workflow | drives the "Link drop" helper |
| `03-execution/05-image-prompts-10-starter-posts.md` | 4 Canva specs + 6 AI image prompts | use to make images, then upload |
| `03-execution/06-partnership-pitch-templates.md` | 5 channels of cold pitches | partnerships (not group posting) |
| `03-execution/07-cca-fact-sheet.md`, `08-wedding-venue-rate-sheet.md` | Partner collateral | partnerships |
| `04-related/01-priority-1-cold-outreach.md` | **22 advertiser prospects** + 3 pitch templates | advertiser sales (see note below) |
| `04-related/02-sentera-bonus-mention-package.md` | Editorial + testimonial sequence | reference |
| duplicate `*-v1.md` files at the `templates_data/` root | same content as the `03-`/`04-` numbered files | duplicates, ignore |

## What's been wired into the dashboard
- **Templates** = the real T1–T8 from the playbook (with each template's keyword).
- **Groups import** now understands the enriched CSV: `audience_archetype` → bucket,
  `recommended_template` honored when generating, plus `recommended_keyword`,
  `pitch_angle`, `red_flag`, `final_tier` stored and shown. Tier C + non-posting
  archetypes import as **inactive** so the rotation focuses on A/B groups.

## Open question — the "advertiser-prospects-with-hooks" CSV
You mentioned a CSV named **`tank-mix-advertiser-prospects-with-hooks`** with hooks
applied to the first 100, to test on. I do **not** see that file in the upload. What
*is* here:
- `01-data/01-fb-groups-enriched.csv` — the **group-posting** list (what we'd use to
  post to groups). No literal per-post "hooks" column, but it has `pitch_angle` +
  `recommended_template` per group, which is effectively the hook source.
- `04-related/01-priority-1-cold-outreach.md` — "advertiser prospects" = companies to
  **sell newsletter ads to**, not groups to post in.

So either (a) that with-hooks CSV is a separate file you still need to upload, or
(b) you meant the enriched groups CSV. **Tell me which** and I'll wire the test list
to it. For now the dashboard is set up on the enriched groups CSV.
