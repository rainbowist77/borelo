"""Time-zone-aware helpers shared by the feed and the site statistics.

Everything the site displays or publishes is expressed in `config.SITE_TIMEZONE`.
Frontmatter may omit the offset (the common case, e.g. `2026-11-08 22:30`);
those values are read as local time in the configured zone rather than as UTC,
which is what the old date-only code silently assumed.
"""

from __future__ import annotations

from datetime import date, datetime, time, timezone
from zoneinfo import ZoneInfo

import config


def zone() -> ZoneInfo:
    return ZoneInfo(config.SITE_TIMEZONE)


def localize(value: datetime) -> datetime:
    """Attach the site zone to a naive datetime; convert aware ones."""
    if value.tzinfo is None:
        return value.replace(tzinfo=zone())
    return value.astimezone(zone())


def parse_moment(value: object) -> datetime | None:
    """Read a frontmatter date/datetime, tolerating several spellings.

    Accepts `date`, `datetime`, and strings such as `2026-11-08`,
    `2026-11-08 22:30`, `2026-11-08T22:30:00` or an already-offset value.
    Naive values are interpreted in the configured site zone.
    """
    if isinstance(value, datetime):
        return localize(value)
    if isinstance(value, date):
        return datetime.combine(value, time.min, tzinfo=zone())
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        try:
            return localize(datetime.fromisoformat(text))
        except ValueError:
            pass
        try:
            return datetime.combine(date.fromisoformat(text[:10]), time.min, tzinfo=zone())
        except ValueError:
            return None
    return None


def from_timestamp(timestamp: float) -> datetime:
    """A filesystem mtime, expressed in the site zone."""
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).astimezone(zone())


def rfc3339(moment: datetime) -> str:
    """RFC 3339 with second precision, e.g. `2026-11-08T22:30:00+08:00`."""
    return localize(moment).replace(microsecond=0).isoformat()


def today() -> date:
    return datetime.now(tz=zone()).date()


def relative_days(value: datetime | date | None) -> str:
    """Human wording for "how long ago", e.g. `今天` / `昨天` / `12 天前`."""
    if value is None:
        return "—"
    if isinstance(value, datetime):
        value = localize(value).date()
    delta = (today() - value).days
    if delta <= 0:
        return "今天"
    if delta == 1:
        return "昨天"
    if delta < 30:
        return f"{delta} 天前"
    if delta < 365:
        months = delta // 30
        return f"{months} 个月前"
    return f"{delta // 365} 年前"
