"""Flask application factory."""

from __future__ import annotations

from flask import Flask, render_template

from app.db import init_db
from app.routes import api, feed, pages


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )
    init_db()

    app.register_blueprint(pages.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(feed.bp)

    @app.errorhandler(404)
    def not_found(_exc):
        return render_template("404.html"), 404

    return app
