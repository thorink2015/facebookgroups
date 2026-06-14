# Tank Mix — Knowledge Base (distilled)

Fast-retrieval summary of the strategy package, so I (and you) don't have to
re-read 28 files. Sources are in `templates_data/` (the uploaded package) and
mapped in `SOURCE-INDEX.md`. This is the short version; the source files are the
long version.

## The goal
Turn ~426 Facebook groups into Tank Mix newsletter subscribers **without burning
the account**. Frame: don't sell the newsletter, drop useful posts that prove you
know the trade; the newsletter is the obvious next step.

## The 4 audience buckets (the CSV's 7 archetypes collapse into these)
| Bucket | Who | Best templates |
|---|---|---|
| `operators` | spray-drone ops, ag-pilot mentorship, drone business | T1, T2, T6, T7, T8 |
| `farmer_operators` | farmer / regional ag / cattle / sprayer-brand groups | T1, T3, T4, T5 |
| `drone_curious` | drone-adjacent, Part 107, DJI/Autel owners | T2, T7, T8 |
| `specialty` | food plot, hunting, beekeeping, organic, specialty crop | T3, T5 |
Non-posting archetypes (`partner`, `editorial`, `decision_influencer`) are imported
**inactive** — they're for outreach, not group posting.

## The 8 templates (full copy lives in templates.json / the playbook)
| Code | Name | Keyword CTA | Image types |
|---|---|---|---|
| T1 | Rate Question (highest engagement) | rates | rate_card, hero |
| T2 | Plain-English Reg Decode | reg | quote_card, hero |
| T3 | Photo Story | (profile link) | hero |
| T4 | Farmer-Ask Dual Hook | yes | quote_card, hero |
| T5 | Tailgate / Send-to-a-buddy | (profile link) | hero |
| T6 | Job Lead / Open Acres | acres | hero |
| T7 | Honest Gear Take | gear | screenshot, hero |
| T8 | DJI Ban / China Watch | DJI | quote_card, hero, screenshot |

## The link mechanic (non-negotiable)
**Never put the subscribe link in the post body** — Facebook suppresses external
links. Instead the post body ends with "Comment '<keyword>' and I'll send it." When
someone comments the keyword, you **reply with the link + DM them**. The comment
boosts the post; the DM is personal. Keywords rotate: rates, reg, gear, DJI, acres,
tank, yes, in, send. (The dashboard's "Link drop" box shows the right keyword + the
reply text per queued post.)

## Image strategy — 4 reusable types
- **hero** — golden-hour T50 + operator shots (from the image prompt pack).
- **rate_card** — Canva table of regional $/acre numbers, magazine pull-quote look.
- **quote_card** — one line from an issue on bone-white, Tank Mix wordmark bottom-right.
- **screenshot** — crop of a Tank Mix issue segment with the date visible.
Square 1080x1080 for in-feed; vertical 1080x1350 for high-engagement. Wordmark in a corner.

## Cadence (the safe rails the dashboard enforces as guardrails)
- Week 1: lurk + comment helpfully, no links. DM admins of top 5 groups.
- Week 2: **3 posts/day**, openers T1 + T3, reply to comments within 2h.
- Week 3+: **5 posts/day**, rotate all 8 templates, expand tiers.
- Hard rules: never the same post in 5 groups same day (rewrite the hook); never post
  in a group you've been in < 7 days; personal profile only (bio: "Founder, Tank Mix");
  never argue in comments. ("Don't try to post in 426 groups. That's how you get banned.")

## CSV columns that drive the dashboard (enriched CSV, 426 rows)
- `final_tier`: A (post regularly, 56) / B (test, 151) / C (skip, 219) → C imported inactive.
- `audience_archetype` → the group's bucket (category).
- `recommended_template` (e.g. "T2 reg decode") → the dashboard honors this first.
- `recommended_keyword` → the per-group comment CTA shown in the queue.
- `pitch_angle` → best angle, shown as a hint.
- `red_flag` → per-group warning, shown as a pre-flight banner before you post.

## Voice rules (never change when optimizing copy)
No em/en dashes. Banned words: leverage, robust, navigate, delve, seamless, crucially,
notably, in conclusion, in essence. Contractions OK. Short punchy sentences. Specific
dollar figures over ranges. Blue-collar plain tone, ~5th–7th grade. No comma before
"and" in compound sentences.

## Credibility numbers worth dropping into posts
16.4M acres drone-sprayed in 2025 (+58.7% YoY, ASDC) · $13/acre 2025 avg rate (ASDC) ·
$12.27/acre farmer-owned at 1,000 ac (Univ Missouri) · 980 ac own-vs-hire break-even ·
$27.26/acre Beck's 2025 PFR corn fungicide ROI · 5,500 FAA-registered ag drones mid-2025 ·
80% of farmers consult a CCA before spraying · 50,000+ Farmer Veteran Coalition members.

## Realistic conversion math (from the playbook)
3 posts/day × 5 days = 15 posts/week → ~8–25 comment opt-ins per useful post →
60–80% convert → ~70–150 new subs/week once rolling. 575 → 1,000 subs in 4–6 weeks.
