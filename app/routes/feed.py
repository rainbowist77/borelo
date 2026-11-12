"""Atom feed route."""

from __future__ import annotations

import config
from flask import Blueprint, Response, render_template, url_for

from app.services import posts, times

bp = Blueprint("feed", __name__)


@bp.get("/feed.atom")
def atom_feed():
    all_posts = posts.load_posts()
    base_url = config.BASE_URL.rstrip("/")
    feed_url = f"{base_url}{url_for('feed.atom_feed')}"

    # The feed's own <updated> is the most recent modification across posts,
    # falling back to publication time when there is nothing else.
    if all_posts:
        feed_updated = times.rfc3339(max(p.updated for p in all_posts))
    else:
        feed_updated = "1970-01-01T00:00:00+00:00"

    rendered = render_template(
        "feed.atom",
        posts=all_posts,
        feed_url=feed_url,
        base_url=base_url,
        feed_updated=feed_updated,
        site_name=config.SITE_NAME,
        site_author=config.SITE_AUTHOR,
        site_description=config.SITE_DESCRIPTION,
    )
    return Response(rendered, mimetype="application/atom+xml; charset=utf-8")
