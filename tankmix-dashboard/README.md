# Tank Mix — Campaign Dashboard

A simple, local dashboard to **plan, organize, and track** your Tank Mix
newsletter promotion in Facebook groups — at a safe, human cadence.

It does the boring parts for you:
- keeps your list of groups and **shows which ones you've already posted to**,
- holds your **8 templates + rotated hook variants** and your **image library**,
- builds a **"do this next" queue** of posts where **no two are identical**,
- gives you **copy-to-clipboard** text + the matched image + the **first-comment**
  link to paste,
- **logs every post** so you never repeat copy or lose your place.

### What it does NOT do (on purpose)
It does **not** log into Facebook, drive a browser, or post for you. **You** click
"Post" in Facebook (a few clicks per group). That one decision is what keeps your
real account safe and keeps you inside your own posting playbook. See
[`docs/DECISIONS-AND-LOG.md`](docs/DECISIONS-AND-LOG.md) for the full why.

---

## Run it (for non-coders)

You need **Python 3** installed ([python.org](https://www.python.org/downloads/) →
"Download", run installer; on Windows tick **"Add Python to PATH"**).

### Mac / Linux
1. Open **Terminal**.
2. Type `cd ` (with a space), then drag the `tankmix-dashboard` folder into the
   window and press **Enter**.
3. Run:
   ```
   ./start.sh
   ```
4. Open your browser to **http://127.0.0.1:5000**

### Windows
1. Open the `tankmix-dashboard` folder.
2. Double-click **`start.bat`**.
3. Open your browser to **http://127.0.0.1:5000**

The first run installs everything automatically (about a minute). Every run after
that is instant. To stop it, press **Ctrl+C** in the Terminal window, or just close it.

---

## First-time setup, in order

1. **Settings tab** → paste your **newsletter link** (it goes in the first comment,
   never the post body) and set your cadence guardrails.
2. **Groups tab** → click **Import CSV** and choose your groups file. Columns can be
   `url, name, category, notes` in any order. (Sample groups are loaded the first
   time so you can look around — delete them once your real ones are in.)
3. **Templates tab** → replace the starter copy with your real T1–T8 hook variants.
4. **Images tab** → upload your images and tag each one (`hero`, `rate_card`,
   `quote_card`, `screenshot`).
5. **Daily Queue tab** → set how many you want, click **Generate**, then work the
   list: open group → paste text → attach the image → Post → add the first comment →
   click **Mark posted**.

---

## Where your stuff lives
- Your data is in **`data/tankmix.db`** (a single file; delete it to start fresh —
  `seed.py` rebuilds it).
- Images you upload go in **`data/images/`**.
- Put your real groups CSV anywhere and import it from the Groups tab. A copy can
  live in `data/` for safekeeping.

## Tabs at a glance
| Tab | What it's for |
|---|---|
| Overview | Stats, what to do next, recent activity, coverage by category |
| Daily Queue | Generate a non-duplicate batch and post it by hand |
| Groups | Import/manage groups, see last-posted + post counts |
| Templates | Your 8 templates and their rotated hook variants |
| Images | Upload + tag the images you rotate through |
| History | Every logged post; export to CSV |
| Settings | Newsletter link + cadence guardrails |
| Logs | What the app recorded + your own notes ("don't repeat this mistake") |

Need help or want to change something? Open this folder in Claude Code — see
[`CLAUDE.md`](CLAUDE.md) for the project context.
