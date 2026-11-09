"""SQLite helpers for post metrics."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path

import config


def _connect() -> sqlite3.Connection:
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(config.DATABASE_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


@contextmanager
def get_db():
    conn = _connect()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> Path:
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS post_metrics (
                slug TEXT PRIMARY KEY,
                views INTEGER NOT NULL DEFAULT 0,
                likes INTEGER NOT NULL DEFAULT 0,
                last_viewed_at TEXT,
                last_liked_at TEXT
            )
            """
        )
    return config.DATABASE_PATH
