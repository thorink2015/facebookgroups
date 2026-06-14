# data/ — your campaign data

## Put your groups CSV here
Drop your real Facebook groups CSV in this folder (any filename), then open the
dashboard → **Groups** tab → **Import CSV**.

**Columns** (any order, header row recommended):
| column | required | example |
|---|---|---|
| `url` | yes | `https://www.facebook.com/groups/123456` |
| `name` | no | `Spray Drone Operators USA` |
| `category` | no | `operators` / `farmer_operators` / `drone_curious` / `specialty` |
| `notes` | no | anything |

If there's no header row, the first column is treated as the URL. Importing is
**additive** — it never deletes, and duplicate URLs are skipped automatically.
URLs are cleaned to a standard form (handles `m.facebook.com`, missing `www`,
trailing tabs, query strings, etc.).

## Other files in here
- `sample_groups.csv` — four fake rows loaded on first run so you can explore.
  Delete those rows in the Groups tab once your real groups are imported.
- `images/` — where uploaded images are stored (managed from the Images tab).
- `tankmix.db` — the local database (created automatically; **not** committed to git).
  Safe to delete to start completely fresh; `seed.py` rebuilds it.
