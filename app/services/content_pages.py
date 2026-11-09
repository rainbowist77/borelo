"""Standalone Markdown pages that are not part of the post stream.

Pages live in `content/pages/<slug>.md` so every authored word stays under
`content/`. The post loader only globs `content/*.md`, so files here are
never picked up as articles.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import frontmatter
import markdown as md

import config

_cache: dict[str, tuple[float, dict[str, Any] | None]] = {}


def _path(slug: str) -> Path:
    return config.PAGES_DIR / f"{slug}.md"


def load_page(slug: str) -> dict[str, Any] | None:
    """Parse a page, or return None when it does not exist."""
    path = _path(slug)
    if not path.is_file():
        return None

    mtime = path.stat().st_mtime
    cached = _cache.get(slug)
    if cached and cached[0] == mtime:
        return cached[1]

    try:
        doc = frontmatter.load(path)
    except Exception:
        return None

    body = doc.content or ""
    page = {
        "slug": slug,
        "title": str(doc.get("title") or slug),
        "summary": str(doc.get("summary") or "").strip(),
        "body_html": md.markdown(
            body,
            extensions=["fenced_code", "tables", "smarty", "toc"],
        ),
    }
    _cache[slug] = (mtime, page)
    return page
