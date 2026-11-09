"""Scan and parse Markdown posts from the content directory."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

import frontmatter
import markdown as md

import config

_cache: dict[str, Any] = {"mtime": None, "posts": []}


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
        return date.fromisoformat(value.strip()[:10])
    return date.today()


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [part.strip() for part in value.split(",") if part.strip()]
    if isinstance(value, (list, tuple)):
        return [str(item).strip() for item in value if str(item).strip()]
    return [str(value).strip()]


def _word_count(text: str) -> int:
    """Count CJK characters plus whitespace-separated Latin tokens."""
    if not text:
        return 0
    cjk = sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")
    latin = [tok for tok in text.split() if any("a" <= c.lower() <= "z" for c in tok if c.isalpha())]
    # Prefer CJK-heavy count; fall back to simple length for mixed/plain text
    stripped = "".join(text.split())
    if cjk:
        non_space = len(stripped)
        return non_space
    return len(text.split()) or len(stripped)


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
        summary = plain[:120] + ("…" if len(plain) > 120 else "")

    return Post(
        slug=slug,
        title=title,
        date=post_date,
        categories=categories,
        tags=tags,
        summary=summary,
        body_html=body_html,
        body_text=body,
        word_count=_word_count(body),
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

    posts: list[Post] = []
    if config.CONTENT_DIR.exists():
        for path in sorted(config.CONTENT_DIR.glob("*.md")):
            item = _load_post(path)
            if item:
                posts.append(item)
    posts.sort(key=lambda p: (p.date, p.slug), reverse=True)
    _cache["mtime"] = mtime
    _cache["posts"] = posts
    return list(posts)


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
