"""Shared Markdown configuration.

Posts and standalone pages render through the same extension set so that any
syntax demonstrated in `content/` behaves identically on `/about/`.

Link handling: authors write paths relative to the site root, e.g.
`![图](/static/uploads/night.svg)`. HTML pages keep them as written. The Atom
feed calls `render(..., base_url=BASE_URL)` so the same markup becomes
absolute — a reader renders the feed's HTML outside our domain, where
root-relative URLs would resolve against the reader's own origin.
"""

from __future__ import annotations

import re

import markdown as md
from markdown.inlinepatterns import SimpleTagInlineProcessor
from markdown.extensions import Extension

import config

EXTENSIONS = [
    # code blocks, tables, lists
    "fenced_code",
    "tables",
    "def_list",
    "sane_lists",
    "abbr",
    # typography
    "smarty",
    # structure
    "toc",
    "attr_list",
    "footnotes",
    "admonition",
    "md_in_html",
]

EXTENSION_CONFIGS = {
    "toc": {
        "permalink": "#",
        "toc_depth": "2-3",
    },
}


class StrikethroughExtension(Extension):
    """`~~text~~` → `<del>text</del>`.

    Core Python-Markdown has no strikethrough and pulling in
    pymdown-extensions for one inline rule is not worth the dependency.
    This mirrors what `pymdownx.tilde` does for the double-tilde case only.
    """

    def extendMarkdown(self, md_instance):  # noqa: N802 - API name
        md_instance.inlinePatterns.register(
            SimpleTagInlineProcessor(r"(~~)(.+?)~~", "del"),
            "strikethrough",
            65,
        )

# <img src="..."> and <a href="..."> written by the Markdown extensions above.
_SRC_RE = re.compile(r'(<(?:img|source)\b[^>]*?\bsrc=")([^"]+)(")', re.IGNORECASE)
_HREF_RE = re.compile(r'(<a\b[^>]*?\bhref=")([^"]+)(")', re.IGNORECASE)


def _needs_origin(url: str) -> bool:
    """True when the URL would resolve against the reader's origin.

    Covers both `uploads/x.png` and `/static/uploads/x.png`: a feed client
    renders the HTML outside our domain, so root-relative paths break there
    exactly like bare relative ones. Absolute URLs, anchors and non-HTTP
    schemes are left untouched.
    """
    return not url.startswith(("http://", "https://", "//", "#", "mailto:", "data:", "tel:"))


def _absolutize(html: str, base_url: str) -> str:
    """Prefix root-relative and bare-relative URLs with the site origin."""
    if not base_url:
        return html

    origin = base_url.rstrip("/")

    def fix(match: re.Match[str]) -> str:
        head, url, tail = match.group(1), match.group(2), match.group(3)
        if not _needs_origin(url):
            return match.group(0)
        if url.startswith("/"):
            return f"{head}{origin}{url}{tail}"
        return f"{head}{origin}/{url}{tail}"

    html = _SRC_RE.sub(fix, html)
    html = _HREF_RE.sub(fix, html)
    return html


def render(text: str, *, base_url: str | None = None) -> str:
    """Render Markdown to HTML.

    `base_url` is only needed for output that leaves the site (the Atom feed).
    Pages rendered for the browser keep relative URLs so they survive a
    misconfigured BASE_URL.
    """
    html = md.markdown(
        text or "",
        extensions=[*EXTENSIONS, StrikethroughExtension()],
        extension_configs=EXTENSION_CONFIGS,
        output_format="html",
    )
    if base_url:
        html = _absolutize(html, base_url)
    return html
