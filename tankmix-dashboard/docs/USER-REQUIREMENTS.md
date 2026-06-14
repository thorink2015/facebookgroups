# What the owner asked for (saved for the record)

## The goal (in plain terms)
Promote the **Tank Mix** newsletter (agricultural spray-drone niche) by posting a
picture + description into a large list of Facebook groups (the owner has ~100,
with CSVs of group links), from their **personal** Facebook profile where they're
already a member of the groups. The owner wants this to be fast, repeatable, and
not feel like a part-time job.

## What the owner originally requested (verbatim intent)
- Auto-post to **50–100 groups per night**, unattended, after 6pm.
- **Maximum stealth** to mimic a human and avoid Facebook detection (variable
  delays between posts, human-like behavior), run over 8–12 hours overnight.
- Run on **Sonnet, not Opus**, to keep cost low during the day job.
- Multiple images + copy, adjusted per group / group type.
- A **dashboard** to watch progress, see errors/logs, stop it, see timing, and
  upload/edit new copy and images to test.
- "Do everything in batches… if you need more research, give me the exact prompt."
- The owner says they did something similar before (with "openclaw") and it worked,
  so they believe ~50/night is feasible and want to test it.

## What we are building instead, and why
We are building a **manual-posting cockpit**, not an auto-poster. The dashboard does
all the *thinking and tracking* (non-duplicate copy, image rotation, who's been
posted to, logs, guardrails); the owner does the *posting* (a few clicks per group).

Reasons (full version in `DECISIONS-AND-LOG.md`):
1. The auto-poster's core is **bot-detection evasion at spam scale** — platform abuse
   we won't build.
2. It **contradicts the owner's own playbook** (≈3–5 posts/day, rewrite hooks,
   "don't post to 426 groups, that's how you get banned").
3. Both of the owner's own research docs admit 50–100/night on one personal profile
   is **above the safe range** and risks a limit/ban with no appeal.

The owner accepted this direction ("go as you decide is best") and asked us to
create the folder + dashboard and a place to upload all docs. That's this repo.

## Useful, non-controversial facts to keep using
- Link policy: **link in the first comment, never the post body.**
- Categories in play: `operators`, `farmer_operators`, `drone_curious`, `specialty`.
- Image types: `hero`, `rate_card`, `quote_card`, `screenshot`.
- Templates: **T1–T8** with multiple hook variants each; never reuse identical copy.
