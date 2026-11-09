"""Atom feed route."""

from __future__ import annotations

from datetime import datetime, timezone

from flask import Blueprint, Response, render_template, url_for

import config
from app.services import posts

bp = Blueprint("feed", __name__)


def _iso_moment(day) -> str:
    """Midnight UTC for a date, as an RFC 3339 timestamp."""
    return datetime(day.year, day.month, day.day, tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


@bp.get("/feed.atom")
def atom_feed():
    all_posts = posts.load_posts()
    base_url = config.BASE_URL.rstrip("/")
    feed_url = f"{base_url}{url_for('feed.atom_feed')}"
    updated = _iso_moment(all_posts[0].date) if all_posts else "1970-01-01T00:00:00Z"

    rendered = render_template(
        "feed.atom",
        posts=all_posts,
        feed_url=feed_url,
        base_url=base_url,
        updated=updated,
        iso_moment=_iso_moment,
        site_name=config.SITE_NAME,
        site_author=config.SITE_AUTHOR,
        site_description=config.SITE_DESCRIPTION,
    )
    return Response(rendered, mimetype="application/atom+xml; charset=utf-8")
