"""
Central configuration for the Tank Mix Campaign Dashboard.

Everything here is plain values you can read and change. No magic.
"""
import os

# Folders -------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
IMAGES_DIR = os.path.join(DATA_DIR, "images")          # where uploaded images live
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates_data")
TEMPLATES_JSON = os.path.join(TEMPLATES_DIR, "templates.json")
DB_PATH = os.path.join(DATA_DIR, "tankmix.db")          # the SQLite database file
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Which image file types we accept on upload
ALLOWED_IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

# Default planning guardrails. You can change all of these in the Settings tab.
# These are ADVISORY only — this tool never posts for you, it only plans and
# tracks what YOU post by hand. The numbers follow the safe-cadence guidance in
# your own Tank Mix posting playbook.
DEFAULT_SETTINGS = {
    # How many groups to put in a single "session" queue when you click Generate.
    "session_target": "5",
    # Soft daily ceiling. The dashboard warns you (does not block) above this.
    "daily_cap": "10",
    # Reminder only: minutes to space posts apart so it reads as human.
    "min_gap_minutes": "8",
    # Don't reuse the same copy variant or image within this many days.
    "dup_window_days": "14",
    # Don't re-post to the same group within this many days.
    "group_cooldown_days": "7",
    # Above this number of posts in a day the UI shows a "high volume" caution.
    "high_volume_warn": "15",
    # Your newsletter link. Per your playbook this goes in the FIRST COMMENT,
    # never in the post body. The queue shows you the comment text to paste.
    "newsletter_link": "",
    "first_comment_text": "Free Tank Mix newsletter (rates, gear, regs): {link}",
}

# Server
HOST = "127.0.0.1"
PORT = int(os.environ.get("TANKMIX_PORT", "5000"))
