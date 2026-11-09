"""Atom feed route."""

from __future__ import annotations

from flask import Blueprint, Response, render_template, url_for

import config
from app.services import posts

bp = Blueprint("feed", __name__)


@bp.get("/feed.atom")
def atom_feed():
    all_posts = posts.load_posts()
    feed_url = f"{config.BASE_URL.rstrip('/')}{url_for('feed.atom_feed')}"
    html = render_template(
        "feed.atom",
        posts=all_posts,
        feed_url=feed_url,
        base_url=config.BASE_URL.rstrip("/"),
        site_name=config.SITE_NAME,
        site_author=config.SITE_AUTHOR,
        site_description=config.SITE_DESCRIPTION,
    )
    return Response(html, mimetype="application/atom+xml; charset=utf-8")
