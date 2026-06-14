"""
Small helpers: Facebook group URL cleanup and CSV parsing.
"""
import csv
import io
import re


def canonicalize_group_url(raw):
    """
    Turn any Facebook group link into a clean, consistent form:
        https://www.facebook.com/groups/<id-or-name>/

    Handles m.facebook.com, missing www, query strings, trailing tabs, etc.
    Returns (clean_url, group_id_or_slug). If it can't find a group id it
    returns the input trimmed so nothing is silently lost.
    """
    if not raw:
        return "", ""
    s = raw.strip()
    # Pull the group identifier out of the path.
    m = re.search(r"facebook\.com/groups/([^/?#]+)", s, re.IGNORECASE)
    if not m:
        # Maybe they pasted just the id/slug.
        slug = s.strip("/ ")
        if slug and "/" not in slug and "." not in slug:
            return f"https://www.facebook.com/groups/{slug}/", slug
        return s, ""
    slug = m.group(1)
    return f"https://www.facebook.com/groups/{slug}/", slug


def parse_groups_csv(file_bytes):
    """
    Read an uploaded CSV of groups. We are forgiving about column names.

    Recognized headers (case-insensitive, any subset):
        url / group_url / link / group_link   -> the group link  (required)
        name / group_name / title             -> a friendly name (optional)
        category / type / tier / segment      -> grouping label  (optional)
        notes                                 -> free text       (optional)

    If there is no header row, the first column is treated as the URL.
    Returns a list of dicts: {url, name, category, notes}.
    """
    text = file_bytes.decode("utf-8-sig", errors="replace")
    sample = text[:2048]
    has_header = False
    try:
        has_header = csv.Sniffer().has_header(sample)
    except Exception:
        has_header = "http" not in sample.split("\n")[0].lower()

    rows = list(csv.reader(io.StringIO(text)))
    rows = [r for r in rows if any((c or "").strip() for c in r)]  # drop blank lines
    if not rows:
        return []

    out = []
    if has_header:
        header = [h.strip().lower() for h in rows[0]]

        def idx(*names):
            for n in names:
                if n in header:
                    return header.index(n)
            return None

        i_url = idx("url", "group_url", "link", "group_link")
        i_name = idx("name", "group_name", "title")
        i_cat = idx("category", "type", "tier", "segment", "audience")
        i_notes = idx("notes", "note", "comment")
        if i_url is None:
            i_url = 0  # fall back to first column
        for r in rows[1:]:
            def cell(i):
                return r[i].strip() if (i is not None and i < len(r)) else ""
            url = cell(i_url)
            if not url:
                continue
            out.append({
                "url": url,
                "name": cell(i_name),
                "category": cell(i_cat) or "uncategorized",
                "notes": cell(i_notes),
            })
    else:
        for r in rows:
            url = (r[0] or "").strip()
            if not url:
                continue
            out.append({
                "url": url,
                "name": r[1].strip() if len(r) > 1 else "",
                "category": (r[2].strip() if len(r) > 2 else "") or "uncategorized",
                "notes": r[3].strip() if len(r) > 3 else "",
            })
    return out
