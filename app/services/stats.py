"""Aggregate site-wide statistics."""

from __future__ import annotations

from datetime import datetime

import config
from app.services import metrics, posts, times


def _parse_iso_moment(value: str | None) -> datetime | None:
    if not value:
        return None
    return times.parse_moment(value)


def site_stats() -> dict:
    all_posts = posts.load_posts()
    categories = posts.all_categories(all_posts)
    tags = posts.all_tags(all_posts)
    total_words = sum(p.word_count for p in all_posts)

    runtime_days = max((times.today() - config.SITE_LAUNCHED).days, 0)

    # "Last activity" is the most recent of a publication, a file edit, or a
    # recorded view/like — compared as moments, not as bare dates.
    candidates: list[datetime] = []
    if all_posts:
        candidates.append(max(p.published for p in all_posts))
        candidates.append(max(p.updated for p in all_posts))
    latest_metric = _parse_iso_moment(metrics.latest_activity_iso())
    if latest_metric:
        candidates.append(latest_metric)

    last_activity = max(candidates) if candidates else None

    return {
        "post_count": len(all_posts),
        "category_count": len(categories),
        "tag_count": len(tags),
        "total_words": total_words,
        "runtime_days": runtime_days,
        "last_activity": times.relative_days(last_activity),
        "categories": categories,
        "tags": tags,
    }
