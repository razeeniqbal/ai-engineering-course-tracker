"""Store UTC, show Malaysia time."""

from datetime import date, datetime, timedelta, timezone

from app.config import settings


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def as_utc(dt: datetime) -> datetime:
    # SQLite drops tzinfo; everything we write is UTC, so naive means UTC.
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)


def to_local(dt: datetime | None) -> datetime | None:
    return None if dt is None else as_utc(dt).astimezone(settings.display_tz)


def local_today() -> date:
    return utcnow().astimezone(settings.display_tz).date()


def week_start(day: date) -> date:
    """Monday of the week containing `day`."""
    return day - timedelta(days=day.weekday())


def format_length(seconds: int | None) -> str:
    if seconds is None:
        return ""
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def parse_length(text: str) -> int:
    """Accept '2:05', '1:02:05' or plain seconds ('125')."""
    text = text.strip()
    if not text:
        raise ValueError("Length is required")
    parts = text.split(":")
    if len(parts) > 3 or not all(p.isdigit() for p in parts):
        raise ValueError("Use m:ss, h:mm:ss or seconds")
    nums = [int(p) for p in parts]
    if len(nums) > 1 and any(n >= 60 for n in nums[1:]):
        raise ValueError("Minutes and seconds must be under 60")
    total = 0
    for n in nums:
        total = total * 60 + n
    if total <= 0:
        raise ValueError("Length must be more than zero")
    return total
