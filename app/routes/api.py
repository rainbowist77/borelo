"""JSON API for views and likes."""

from __future__ import annotations

from flask import Blueprint, jsonify

from app.services import metrics, posts

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.get("/metrics/<slug>")
def get_metrics(slug: str):
    if not posts.get_post(slug):
        return jsonify({"error": "not found"}), 404
    return jsonify(metrics.get_metrics(slug))


@bp.post("/view/<slug>")
def view_post(slug: str):
    if not posts.get_post(slug):
        return jsonify({"error": "not found"}), 404
    return jsonify(metrics.increment_view(slug))


@bp.post("/like/<slug>")
def like_post(slug: str):
    if not posts.get_post(slug):
        return jsonify({"error": "not found"}), 404
    return jsonify(metrics.increment_like(slug))
