# Tank Mix Facebook Strategy: Complete Package

Everything from 6 batches of research and 10 execution artifacts, organized into one navigable package. Designed so you can find any piece of research or any deliverable quickly, and optimize the copy iteratively.

---

## Package contents

```
tank-mix-facebook-package/
├── 00-README-master-index.md        ← you are here
├── 01-data/
│   └── 01-fb-groups-enriched.csv    ← 426 groups + 8 research-derived columns
├── 02-research/
│   └── 01-research-master-consolidated.md  ← all 6 batches in one navigable doc
├── 03-execution/                    ← stuff you actually use to post
│   ├── 01-facebook-posting-playbook.md     ← the original strategy doc with 8 templates
│   ├── 02-top-50-groups-mapped.md          ← the A1-A50 list with real URLs
│   ├── 03-personal-profile-setup.md        ← bio/photo/cover/pinned post specs
│   ├── 04-keyword-optin-mechanic.md        ← 9 keywords, DM templates, workflow
│   ├── 05-image-prompts-10-starter-posts.md ← 4 Canva specs + 6 AI prompts
│   ├── 06-partnership-pitch-templates.md   ← 5 channels of cold pitches
│   ├── 07-cca-fact-sheet.md                ← Channel 1 collateral
│   └── 08-wedding-venue-rate-sheet.md      ← Channel 2 collateral
└── 04-related/                      ← Tank Mix work that touches the FB strategy
    ├── 01-priority-1-cold-outreach.md      ← 22 advertiser prospects, 3 pitch templates
    └── 02-sentera-bonus-mention-package.md ← editorial copy + testimonial sequence
```

---

## Where to find what

### "I'm about to post in Group X. What do I need to know?"
1. Open **01-data/01-fb-groups-enriched.csv** and find the group row.
2. Read the columns: final_tier, recommended_action, pitch_angle, recommended_template, recommended_keyword, red_flag.
3. If you want deeper context on the audience cluster, open **02-research/01-research-master-consolidated.md** → section 4 (Audience Cluster Deep-Dive).
4. Grab the actual post template copy from **03-execution/01-facebook-posting-playbook.md**.
5. Grab the image from **03-execution/05-image-prompts-10-starter-posts.md** (or build a new one in that style).
6. Run the keyword opt-in workflow from **03-execution/04-keyword-optin-mechanic.md**.

### "I'm setting up my profile for the first time."
Open **03-execution/03-personal-profile-setup.md**. 11 sections, 90 minutes of work to do right.

### "I'm sending a CCA outreach email."
1. Read **03-execution/06-partnership-pitch-templates.md** Channel 1 for the email.
2. Personalize using the framework in that file.
3. Have **03-execution/07-cca-fact-sheet.md** ready as a PDF before sending (so you can reply within 24 hours when they ask).

### "I'm sending a wedding venue outreach email."
1. Read **03-execution/06-partnership-pitch-templates.md** Channel 2.
2. Have **03-execution/08-wedding-venue-rate-sheet.md** ready as a PDF.

### "I want to optimize a post's copy."
1. Pull the audience cluster section from **02-research/01-research-master-consolidated.md** for the vocabulary and post patterns that win.
2. Pull the cited numbers from section 7 (Industry Data and $/acre Benchmarks) of that same doc.
3. Apply the voice rules in section 3 of that doc.

### "I'm thinking about Tank Mix advertisers."
Open **04-related/01-priority-1-cold-outreach.md**. 22 prospects, 3 pitch templates (Blast / Recurring / Media swap), 5 pre-personalized examples ready to send.

---

## The CSV columns explained

The enriched CSV has 22 columns. The 14 original columns from your master list, plus 8 research-derived columns:

**Original columns:** Tier, Category, Group Name, Facebook URL, Geography, Primary Audience, Approx Members, Privacy, Activity Level, Why Relevant, Self-Promo Allowed, Admin/Dealer-Run, Source Batch, URL Type.

**New research-derived columns:**
- **final_tier**: A (post regularly), B (test/lurk), C (skip). 56 A, 151 B, 219 C.
- **recommended_action**: Join+Post, Join+Lurk, Comment+DM, Skip, etc. 10 distinct actions.
- **pitch_angle**: One-line of the BEST content angle for that specific group.
- **recommended_template**: Which of the 8 templates (T1-T8) fits this audience best.
- **recommended_keyword**: Which keyword (RATES, REG, GEAR, DJI, ACRES, TANK, SEND, HOW, YES) to use in the comment CTA.
- **audience_archetype**: One of 7 (Operators, Farmer-operator, Drone-curious, Specialty, B2B service buyer/partner, Decision-influencer, Editorial partner).
- **red_flag**: One-line warning specific to that group (link-hostile, brand-controlled, drift-sensitive, etc.).
- **research_batch**: Which of the 6 batches (1-6) covered this group.

Filter the CSV by final_tier = A to get your 56 priority groups. Sort by recommended_action to plan your weekly cadence. Use the red_flag column as your pre-flight check before any post.

---

## How to optimize copy from here

You wanted "organised very well so we can later optimise the copy really well." Here is the optimization workflow:

**1. Pick one audience cluster to optimize at a time.**
Don't try to optimize across all 7 archetypes simultaneously. Pick Operators OR Specialty Crop OR Decision-Influencers. Spend a week on one.

**2. Pull the cluster's research section.**
02-research/01-research-master-consolidated.md → section 4.x for that cluster. Read it cold even though you wrote it. Look for vocabulary patterns and post formats that win.

**3. Filter the CSV.**
Filter for final_tier = A AND audience_archetype = [your cluster]. That's your post-target list for the week.

**4. Generate 3 hook variants per template.**
For each template (T1-T8), write 3 variations of the opening line. Same body, same CTA, different first 8 words. Save in a Google Doc next to the master playbook.

**5. A/B test only the hook.**
Hold body and CTA constant. Post variant A in one A-tier group, variant B in another A-tier group in the same cluster on the same day. Wait 48 hours. Whichever clears 10+ comments wins.

**6. Update the master playbook.**
When a hook beats the original by 2x or more, replace the master template with the new winning hook. Version control: rename the file with -v2, -v3 as you iterate. Keep old versions for reference.

**7. Iterate on red flags.**
The red_flag column in the CSV is your best learning signal. After 30 days of posting, update the red_flag for each group based on what actually happened. Was it really link-hostile? Did the admin actually pull your post? Did anyone reply? Refine.

---

## The voice rules (non-negotiable, applied to every file in this package)

- No em dashes, no double dashes, no en dashes
- Banned words: leverage, robust, navigate, delve, seamless, crucially, notably, in conclusion, in essence
- Contractions allowed
- Short punchy sentences
- Specific dollar figures over ranges
- Blue-collar plain direct tone, fifth-to-seventh grade reading level
- No comma before "and" in compound sentences
- No AI-detectable phrasing

When optimizing copy, the voice rules are the ONE thing that does not change.

---

## Numbers worth memorizing

These appear across multiple files in this package. They are your credibility anchors in every post and pitch:

| Number | What it means | Source |
|---|---|---|
| 16.4M acres | 2025 US drone-sprayed acreage (+58.7% YoY) | ASDC |
| $13/acre | 2025 national average drone spray rate | ASDC |
| $12.27/acre | Farmer-owned cost at 1,000 acres | Univ Missouri G1274 |
| 980 acres | Break-even for owning vs custom hire | Univ Missouri G1274 |
| $27.26/acre | Beck's 2025 PFR drone fungicide ROI on corn | Beck's PFR |
| $25-60K | New ag spray drone price range | Industry |
| $150K-500K+ | Self-propelled ground rig price | Industry |
| 5,500 | FAA-registered ag drones mid-2025 (up from ~1,000 Jan 2024) | MSU/Science |
| $20/acre | Drone mosquito larvicide rate | Vermont BLSG |
| $42/acre | Manned aerial larvicide rate (for comparison) | Vermont BLSG |
| 80% | Farmers who consult a CCA before spraying | Peer-reviewed (Iowa) |
| 25-30% | Farmers who rely fully on CCA | Same source |
| 50,000+ | Farmer Veteran Coalition members | FVC, Aug 2024 |
| 49 / 46 | EPA-labeled hemp pesticides / biopesticides | US EPA |

---

## What's NOT in this package (and what to do about it)

- **Tank Mix issue archive**: not included. You manage that in Beehiiv.
- **Local Ag Drones agency content**: not included. That's a separate business.
- **Directory operator data**: not included. That lives in your operator CSVs.
- **Email infrastructure (warmup logs, sender reputation)**: not included. Manage in Mailtrack / Mailsuite.
- **Final designed PDFs (rate card, partner deck)**: the markdown sources are here but the PDF design needs Canva or a designer.

---

## Versioning

Everything in this package is v1, dated June 14, 2026. As you iterate:

- Don't overwrite. Save as v2, v3 with the date in the file (e.g. `01-facebook-posting-playbook-v2-2026-07-15.md`).
- Keep the CSV as a single living document (update in place but back up monthly).
- Replace the README only when the folder structure changes.

---

## Quick start (today, 2 hours)

1. **Open the CSV** (`01-data/01-fb-groups-enriched.csv`). Filter for final_tier = A. That's your 56 priority groups.
2. **Open the Top 50 mapping** (`03-execution/02-top-50-groups-mapped.md`). Click through and Join/Follow every URL. 25 minutes.
3. **Set up your profile** per `03-execution/03-personal-profile-setup.md`. 90 minutes.

That gets you to launch-ready. Then next Monday: post starter Post 1 in A1 using the keyword opt-in workflow.

The whole rest of the package is reference, optimization, and partnership infrastructure that supports the ongoing posting.
