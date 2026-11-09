"""Flask application factory."""

from __future__ import annotations

from flask import Flask, render_template

from app.db import init_db
from app.routes import api, feed, pages

_ROMAN = (
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
)


def to_roman(value: int) -> str:
    """Render an integer as Roman numerals (1–3999), else decimal."""
    try:
        value = int(value)
    except (TypeError, ValueError):
        return str(value)
    if not 0 < value < 4000:
        return str(value)
    out = []
    for number, glyph in _ROMAN:
        while value >= number:
            out.append(glyph)
            value -= number
    return "".join(out)


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )
    init_db()

    app.add_template_filter(to_roman, "roman")

    app.register_blueprint(pages.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(feed.bp)

    @app.errorhandler(404)
    def not_found(_exc):
        return render_template("404.html"), 404

    return app
