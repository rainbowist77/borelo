"""Site configuration for borelo."""

from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# ── identity ──────────────────────────────────────────────────────────
SITE_NAME = "borelo"
SITE_AUTHOR = "borelo"
SITE_DESCRIPTION = "文字与影子之间"

# Shown inside the cover plate, under the title.
SITE_TAGLINE = "a quiet journal"
# Latin line inside the plate, above the rule.
SITE_EDITION = "private edition"

SITE_LAUNCHED = date(2026, 11, 9)
SITE_TIMEZONE = "Asia/Shanghai"

# Absolute origin used for Atom IDs and links. Must be the public URL in
# production, e.g. "https://borelo.example.com".
BASE_URL = "http://localhost"

# ── paths ─────────────────────────────────────────────────────────────
CONTENT_DIR = ROOT / "content"
# Standalone pages (e.g. about.md). Kept separate so the post loader,
# which globs content/*.md, never treats them as articles.
PAGES_DIR = CONTENT_DIR / "pages"
DATA_DIR = ROOT / "data"
DATABASE_PATH = DATA_DIR / "blog.sqlite"

# ── behaviour ─────────────────────────────────────────────────────────
# How many posts on the home page
HOME_POST_LIMIT = 10
# Characters in an auto-generated summary when frontmatter omits one
SUMMARY_LENGTH = 120
