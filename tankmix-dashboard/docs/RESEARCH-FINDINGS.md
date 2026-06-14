# Research findings that shape the build

This keeps the **safety-relevant conclusions** from the owner's research and
playbook — the parts the dashboard is designed around. (The raw research docs,
including the parts about automation/stealth that we are **not** implementing, can be
uploaded by the owner to `docs/research/` for their own records.)

## Cadence & volume (the numbers that matter)
- The owner's own playbook cadence: **~3–5 posts/day**, and explicitly *"don't try to
  post in 426 groups — that's how you get banned."*
- Community-reported "safe" ranges (vendor sources, treat as soft estimates):
  new accounts ~10–15 groups/day; established (3–6 mo) ~35–50/day; veteran ~100/day.
- **Velocity matters as much as count.** Jumping from a 3/day average to 50 reads as
  anomalous on its own. Guidance: increase by **no more than ~20–30% per week**.
- Block ladder (directional, not official): 24h → 3 days → 1 week → up to 30 days for
  repeats; a block in one group can stop posting in *all* groups during the penalty.
- **Conclusion baked into the dashboard:** default session size and a soft daily cap
  with a "high volume" warning, a per-group cooldown, and a duplicate window — all
  editable, all advisory. The tool nudges toward slow + varied.

## What actually gets accounts blocked
- **Duplicate content** across groups, and **spam reports** from admins/members.
- **Conclusion:** the generator never reuses the same copy variant or image inside a
  configurable window, matches copy to the group's audience, and rotates images.

## Posting mechanics (kept as reference for the manual flow)
- Link goes in the **first comment**, never the body. The Daily Queue shows the
  exact first-comment text to paste.
- Post to a group's normal discussion composer; some groups require topic tags or
  send posts to "pending approval" — those are normal and handled by the human.

## Why "official numbers" don't exist
Facebook does not publish group posting limits; everything above is community
estimate and varies per account. That uncertainty is exactly why the safe move is
human-paced posting with heavy content variety, which is what this tool supports.
