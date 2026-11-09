"""HTML page routes."""

from __future__ import annotations

from flask import Blueprint, abort, render_template

import config
from app.services import content_pages, metrics, posts, stats

bp = Blueprint("pages", __name__)


@bp.app_context_processor
def inject_globals():
    return {
        "site_name": config.SITE_NAME,
        "site_author": config.SITE_AUTHOR,
        "site_description": config.SITE_DESCRIPTION,
        "site_tagline": config.SITE_TAGLINE,
        "site_edition": config.SITE_EDITION,
        "site_launched_year": config.SITE_LAUNCHED.strftime("%Y"),
        "site_timezone": config.SITE_TIMEZONE,
        "site_stats": stats.site_stats(),
    }


@bp.get("/")
def index():
    all_posts = posts.load_posts()
    listed = all_posts[: config.HOME_POST_LIMIT]
    metric_map = metrics.get_metrics_map([p.slug for p in listed])
    return render_template("index.html", posts=listed, metrics=metric_map)


@bp.get("/post/<slug>/")
def post_detail(slug: str):
    post = posts.get_post(slug)
    if not post:
        abort(404)
    metric = metrics.get_metrics(slug)
    return render_template("post.html", post=post, metric=metric)


@bp.get("/about/")
def about():
    page = content_pages.load_page("about")
    if not page:
        abort(404)
    return render_template("page.html", page=page)


@bp.get("/archive/")
def archive():
    tree = posts.archive_tree()
    return render_template("archive.html", tree=tree)


@bp.get("/categories/")
def categories():
    return render_template("categories.html", categories=posts.all_categories())


@bp.get("/category/<name>/")
def category_detail(name: str):
    listed = posts.posts_by_category(name)
    if not listed:
        abort(404)
    metric_map = metrics.get_metrics_map([p.slug for p in listed])
    return render_template(
        "term.html",
        term_type="分类",
        term_kicker="Category",
        term_name=name,
        posts=listed,
        metrics=metric_map,
    )


@bp.get("/tags/")
def tags():
    return render_template("tags.html", tags=posts.all_tags())


@bp.get("/tag/<name>/")
def tag_detail(name: str):
    listed = posts.posts_by_tag(name)
    if not listed:
        abort(404)
    metric_map = metrics.get_metrics_map([p.slug for p in listed])
    return render_template(
        "term.html",
        term_type="标签",
        term_kicker="Tag",
        term_name=name,
        posts=listed,
        metrics=metric_map,
    )
