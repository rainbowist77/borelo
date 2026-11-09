"""Site configuration for borelo."""

from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SITE_NAME = "borelo"
SITE_AUTHOR = "borelo"
SITE_DESCRIPTION = "文字与影子之间的个人笔记"
SITE_LAUNCHED = date(2026, 11, 9)
BASE_URL = "http://localhost"
TIMEZONE = "Asia/Shanghai"

CONTENT_DIR = ROOT / "content"
DATA_DIR = ROOT / "data"
DATABASE_PATH = DATA_DIR / "blog.sqlite"

# How many posts on the home page
HOME_POST_LIMIT = 10
