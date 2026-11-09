"""Aggregate site-wide statistics."""

from __future__ import annotations

from datetime import date, datetime

import config
from app.services import metrics, posts


def _parse_iso_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except ValueError:
        try:
            return date.fromisoformat(value[:10])
        except ValueError:
            return None


def site_stats() -> dict:
    all_posts = posts.load_posts()
    categories = posts.all_categories(all_posts)
    tags = posts.all_tags(all_posts)
    total_words = sum(p.word_count for p in all_posts)

    today = date.today()
    runtime_days = max((today - config.SITE_LAUNCHED).days, 0)

    latest_post_date = all_posts[0].date if all_posts else None
    latest_metric = _parse_iso_date(metrics.latest_activity_iso())
    candidates = [d for d in (latest_post_date, latest_metric) if d]
    last_activity = max(candidates) if candidates else None

    return {
        "post_count": len(all_posts),
        "category_count": len(categories),
        "tag_count": len(tags),
        "total_words": total_words,
        "runtime_days": runtime_days,
        "last_activity": last_activity.isoformat() if last_activity else "—",
        "categories": categories,
        "tags": tags,
    }
