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
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    url         TEXT UNIQUE NOT NULL,
    name        TEXT,
    category    TEXT DEFAULT 'uncategorized',
    fb_id       TEXT,
    notes       TEXT,
    active      INTEGER DEFAULT 1,
    created_at  TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS templates (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    code        TEXT UNIQUE NOT NULL,
    name        TEXT,
    audiences   TEXT,        -- comma separated categories this template fits
    image_types TEXT,        -- comma separated image types this template uses
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


def init_db():
    """Create tables and default settings if they do not exist yet."""
    os.makedirs(config.DATA_DIR, exist_ok=True)
    os.makedirs(config.IMAGES_DIR, exist_ok=True)
    with get_db() as db:
        db.executescript(SCHEMA)
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
