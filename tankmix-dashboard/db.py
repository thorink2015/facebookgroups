"""
Database layer for the Tank Mix Campaign Dashboard.

Uses SQLite (built into Python, no server to install). One file on disk:
data/tankmix.db. Safe to delete that file to start fresh.
"""
import os
import sqlite3
from contextlib import contextmanager

import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS groups (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    url          TEXT UNIQUE NOT NULL,
    name         TEXT,
    category     TEXT DEFAULT 'uncategorized',  -- audience bucket
    fb_id        TEXT,
    notes        TEXT,
    tier         TEXT,        -- A / B / C from the enriched CSV (final_tier)
    rec_template TEXT,        -- recommended template code (e.g. T2) for this group
    keyword      TEXT,        -- recommended comment-keyword CTA for this group
    pitch_angle  TEXT,        -- best content angle for this specific group
    red_flag     TEXT,        -- pre-flight warning for this group
    active       INTEGER DEFAULT 1,
    created_at   TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS templates (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    code        TEXT UNIQUE NOT NULL,
    name        TEXT,
    audiences   TEXT,        -- comma separated audience buckets this template fits
    image_types TEXT,        -- comma separated image types this template uses
    keyword     TEXT,        -- default comment-keyword CTA for this template
    active      INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS variants (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    template_id  INTEGER NOT NULL,
    text         TEXT NOT NULL,
    active       INTEGER DEFAULT 1,
    times_used   INTEGER DEFAULT 0,
    last_used_at TEXT,
    FOREIGN KEY(template_id) REFERENCES templates(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS images (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    filename     TEXT NOT NULL,
    image_type   TEXT DEFAULT 'hero',
    caption      TEXT,
    active       INTEGER DEFAULT 1,
    times_used   INTEGER DEFAULT 0,
    last_used_at TEXT,
    uploaded_at  TEXT DEFAULT (datetime('now'))
);

-- One row per planned/posted item. The "queue" is just rows with status='planned'.
CREATE TABLE IF NOT EXISTS posts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id        INTEGER,
    template_id     INTEGER,
    variant_id      INTEGER,
    image_id        INTEGER,
    copy_text       TEXT,
    status          TEXT DEFAULT 'planned',  -- planned | posted | skipped | failed
    post_url        TEXT,
    link_in_comment INTEGER DEFAULT 0,
    notes           TEXT,
    generated_at    TEXT DEFAULT (datetime('now')),
    posted_at       TEXT
);

CREATE TABLE IF NOT EXISTS settings (
    key   TEXT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS event_log (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    ts      TEXT DEFAULT (datetime('now')),
    level   TEXT DEFAULT 'info',   -- info | warn | error
    message TEXT
);
"""


def _connect():
    # timeout lets a write wait briefly instead of failing instantly if the
    # file is momentarily busy.
    conn = sqlite3.connect(config.DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def get_db():
    """Use as:  with get_db() as db: db.execute(...)"""
    conn = _connect()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# Columns added after the first release. Safe to run every startup: we only add
# a column if it's missing, so older databases get upgraded without losing data.
_MIGRATIONS = {
    "groups": ["tier", "rec_template", "keyword", "pitch_angle", "red_flag"],
    "templates": ["keyword"],
}


def _migrate(db):
    for table, columns in _MIGRATIONS.items():
        existing = {r["name"] for r in db.execute(f"PRAGMA table_info({table})")}
        for col in columns:
            if col not in existing:
                db.execute(f"ALTER TABLE {table} ADD COLUMN {col} TEXT")


def init_db():
    """Create tables, run migrations, and set default settings if missing."""
    os.makedirs(config.DATA_DIR, exist_ok=True)
    os.makedirs(config.IMAGES_DIR, exist_ok=True)
    with get_db() as db:
        db.executescript(SCHEMA)
        _migrate(db)
        for key, value in config.DEFAULT_SETTINGS.items():
            db.execute(
                "INSERT OR IGNORE INTO settings(key, value) VALUES (?, ?)",
                (key, value),
            )


def get_settings():
    with get_db() as db:
        rows = db.execute("SELECT key, value FROM settings").fetchall()
    return {r["key"]: r["value"] for r in rows}


def set_setting(key, value):
    with get_db() as db:
        db.execute(
            "INSERT INTO settings(key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, str(value)),
        )


def log_event(message, level="info"):
    with get_db() as db:
        db.execute(
            "INSERT INTO event_log(level, message) VALUES (?, ?)",
            (level, message),
        )
