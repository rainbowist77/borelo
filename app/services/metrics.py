"""Read and write per-post view / like counters."""

from __future__ import annotations

from datetime import datetime, timezone

from app.db import get_db


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def get_metrics(slug: str) -> dict[str, int | str | None]:
    with get_db() as conn:
        row = conn.execute(
            "SELECT views, likes, last_viewed_at, last_liked_at FROM post_metrics WHERE slug = ?",
            (slug,),
        ).fetchone()
    if not row:
        return {"views": 0, "likes": 0, "last_viewed_at": None, "last_liked_at": None}
    return {
        "views": int(row["views"]),
        "likes": int(row["likes"]),
        "last_viewed_at": row["last_viewed_at"],
        "last_liked_at": row["last_liked_at"],
    }


def get_metrics_map(slugs: list[str]) -> dict[str, dict[str, int]]:
    if not slugs:
        return {}
    placeholders = ",".join("?" for _ in slugs)
    with get_db() as conn:
        rows = conn.execute(
            f"SELECT slug, views, likes FROM post_metrics WHERE slug IN ({placeholders})",
            slugs,
        ).fetchall()
    result = {slug: {"views": 0, "likes": 0} for slug in slugs}
    for row in rows:
        result[row["slug"]] = {"views": int(row["views"]), "likes": int(row["likes"])}
    return result


def increment_view(slug: str) -> dict[str, int | str | None]:
    now = _now_iso()
    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO post_metrics (slug, views, likes, last_viewed_at)
            VALUES (?, 1, 0, ?)
            ON CONFLICT(slug) DO UPDATE SET
                views = views + 1,
                last_viewed_at = excluded.last_viewed_at
            """,
            (slug, now),
        )
    return get_metrics(slug)


def increment_like(slug: str) -> dict[str, int | str | None]:
    now = _now_iso()
    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO post_metrics (slug, views, likes, last_liked_at)
            VALUES (?, 0, 1, ?)
            ON CONFLICT(slug) DO UPDATE SET
                likes = likes + 1,
                last_liked_at = excluded.last_liked_at
            """,
            (slug, now),
        )
    return get_metrics(slug)


def latest_activity_iso() -> str | None:
    with get_db() as conn:
        row = conn.execute(
            """
            SELECT MAX(ts) AS latest FROM (
                SELECT last_viewed_at AS ts FROM post_metrics WHERE last_viewed_at IS NOT NULL
                UNION ALL
                SELECT last_liked_at AS ts FROM post_metrics WHERE last_liked_at IS NOT NULL
            )
            """
        ).fetchone()
    return row["latest"] if row and row["latest"] else None
