"""Scan and parse Markdown posts from the content directory."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

import frontmatter
import markdown as md

import config

_cache: dict[str, Any] = {"mtime": None, "posts": []}

# CJK ideographs, kana and hangul all count as one "character" each.
_CJK_RE = re.compile(r"[぀-ヿ㐀-䶿一-鿿가-힯]")
_LATIN_RE = re.compile(r"[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*")


@dataclass
class Post:
    slug: str
    title: str
    date: date
    categories: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    summary: str = ""
    body_html: str = ""
    body_text: str = ""
    word_count: int = 0
    path: Path | None = None

    @property
    def date_iso(self) -> str:
        return self.date.isoformat()


def _parse_date(value: Any) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str) and value.strip():
        try:
            return date.fromisoformat(value.strip()[:10])
        except ValueError:
            return date.today()
    return date.today()


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [part.strip() for part in value.split(",") if part.strip()]
    if isinstance(value, (list, tuple)):
        return [str(item).strip() for item in value if str(item).strip()]
    return [str(value).strip()]


def word_count(text: str) -> int:
    """Count CJK characters plus Latin/numeric word tokens.

    Chinese is counted per character; Latin runs are counted per word, so
    "hello world" is 2 rather than 10. This keeps the footer number honest
    for mixed-language posts.
    """
    if not text:
        return 0
    cjk = len(_CJK_RE.findall(text))
    latin = len(_LATIN_RE.findall(_CJK_RE.sub(" ", text)))
    return cjk + latin


def _load_post(path: Path) -> Post | None:
    try:
        post = frontmatter.load(path)
    except Exception:
        return None

    slug = path.stem
    title = str(post.get("title") or slug)
    post_date = _parse_date(post.get("date"))
    categories = _as_list(post.get("categories") or post.get("category"))
    tags = _as_list(post.get("tags") or post.get("tag"))
    summary = str(post.get("summary") or "").strip()
    body = post.content or ""
    body_html = md.markdown(
        body,
        extensions=["fenced_code", "tables", "smarty", "toc"],
    )
    if not summary:
        plain = " ".join(body.split())
        limit = config.SUMMARY_LENGTH
        summary = plain[:limit] + ("…" if len(plain) > limit else "")

    return Post(
        slug=slug,
        title=title,
        date=post_date,
        categories=categories,
        tags=tags,
        summary=summary,
        body_html=body_html,
        body_text=body,
        word_count=word_count(body),
        path=path,
    )


def _content_mtime() -> float | None:
    if not config.CONTENT_DIR.exists():
        return None
    mtimes = [p.stat().st_mtime for p in config.CONTENT_DIR.glob("*.md")]
    return max(mtimes) if mtimes else None


def load_posts(*, force: bool = False) -> list[Post]:
    mtime = _content_mtime()
    if not force and _cache["posts"] and _cache["mtime"] == mtime:
        return list(_cache["posts"])

    collected: list[Post] = []
    if config.CONTENT_DIR.exists():
        for path in sorted(config.CONTENT_DIR.glob("*.md")):
            item = _load_post(path)
            if item:
                collected.append(item)
    collected.sort(key=lambda p: (p.date, p.slug), reverse=True)
    _cache["mtime"] = mtime
    _cache["posts"] = collected
    return list(collected)


def get_post(slug: str) -> Post | None:
    for post in load_posts():
        if post.slug == slug:
            return post
    return None


def posts_by_category(name: str) -> list[Post]:
    return [p for p in load_posts() if name in p.categories]


def posts_by_tag(name: str) -> list[Post]:
    return [p for p in load_posts() if name in p.tags]


def archive_tree(posts: list[Post] | None = None) -> dict[int, dict[int, list[Post]]]:
    tree: dict[int, dict[int, list[Post]]] = {}
    for post in posts or load_posts():
        tree.setdefault(post.date.year, {}).setdefault(post.date.month, []).append(post)
    return tree


def all_categories(posts: list[Post] | None = None) -> dict[str, int]:
    counts: dict[str, int] = {}
    for post in posts or load_posts():
        for name in post.categories:
            counts[name] = counts.get(name, 0) + 1
    return dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))


def all_tags(posts: list[Post] | None = None) -> dict[str, int]:
    counts: dict[str, int] = {}
    for post in posts or load_posts():
        for name in post.tags:
            counts[name] = counts.get(name, 0) + 1
    return dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))
