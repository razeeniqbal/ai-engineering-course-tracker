"""Derived numbers for the dashboard, episode and module pages: rings, pace, streak,
activity feed and the weekly study chart. Everything here is read-only."""

import math
from collections import Counter
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.importer import active_version
from app.models import (
    STATUS_LABELS, STATUSES, Episode, EpisodeProgress, Module, ModuleProgress, ProductionTime, StatusEvent,
    StudySession,
)
from app.timeutil import as_utc, local_today, to_local, week_start

WEEKLY_TARGET = 3
STAGE = {slug: i for i, (slug, _) in enumerate(STATUSES)}  # not_started=0 … published=4
LAST_STAGE = len(STATUSES) - 1


def pct(part: float, whole: float) -> int:
    return round(100 * part / whole) if whole else 0


# --- rings ----------------------------------------------------------------------

@dataclass
class Ring:
    key: str
    label: str
    percent: int
    detail: str


def rings(statuses: list[str], module_checks: list[ModuleProgress], module_count: int) -> list[Ring]:
    """Three Activity-style rings: learning (module ticks), production (stage progress), publishing."""
    total = len(statuses)
    published = sum(s == "published" for s in statuses)
    stage_points = sum(STAGE[s] for s in statuses)
    ticks = sum(int(m.learned) + int(m.built) + int(m.tested) for m in module_checks)
    return [
        Ring("learn", "Learn", pct(ticks, module_count * 3), f"{ticks}/{module_count * 3} module ticks"),
        Ring("produce", "Produce", pct(stage_points, total * LAST_STAGE), "stages done across all episodes"),
        Ring("publish", "Publish", pct(published, total), f"{published}/{total} episodes published"),
    ]


# --- pace -----------------------------------------------------------------------

@dataclass
class Pace:
    this_week: int
    target: int
    per_week: float  # recent pace, episodes/week
    remaining: int
    finish_at_pace: date | None
    finish_at_target: date | None


def pace(published_dates: list[date], remaining: int, today: date | None = None) -> Pace:
    today = today or local_today()
    start = week_start(today)
    this_week = sum(start <= d <= today for d in published_dates)
    # Pace over the last 4 weeks; before that much history exists, since the first publish.
    window_start = today - timedelta(days=27)
    recent = [d for d in published_dates if d >= window_start]
    if published_dates and min(published_dates) > window_start:
        weeks = max(1.0, ((today - min(published_dates)).days + 1) / 7)
    else:
        weeks = 4.0
    per_week = round(len(recent) / weeks, 1) if recent else 0.0

    def finish(rate: float) -> date | None:
        if remaining == 0:
            return today
        return today + timedelta(weeks=math.ceil(remaining / rate)) if rate > 0 else None

    return Pace(this_week, WEEKLY_TARGET, per_week, remaining, finish(per_week), finish(WEEKLY_TARGET))


# --- streak ---------------------------------------------------------------------

def streak(active_days: set[date], today: date | None = None) -> int:
    """Consecutive days with any logged activity, ending today (or yesterday if today is still empty)."""
    today = today or local_today()
    day = today if today in active_days else today - timedelta(days=1)
    count = 0
    while day in active_days:
        count += 1
        day -= timedelta(days=1)
    return count


# --- activity feed --------------------------------------------------------------

@dataclass
class Activity:
    at: datetime  # UTC, for ordering
    kind: str  # "status" or "study"
    title: str
    detail: str
    href: str
    status: str | None = None


def activity(db: Session, limit: int = 10) -> list[Activity]:
    version = active_version(db)
    if version is None:
        return []
    episodes = {e.episode_key: e for e in db.scalars(select(Episode).where(Episode.version_id == version.id))}
    modules = {m.module_key: m for m in db.scalars(select(Module).where(Module.version_id == version.id))}
    items: list[Activity] = []
    for ev in db.scalars(select(StatusEvent).order_by(StatusEvent.changed_at.desc()).limit(limit)):
        ep = episodes.get(ev.episode_key)
        if ep:
            items.append(Activity(as_utc(ev.changed_at), "status", f"{ep.code} · {ep.title}",
                                  f"{STATUS_LABELS[ev.from_status]} → {STATUS_LABELS[ev.to_status]}",
                                  f"/episodes/{ep.episode_key}", ev.to_status))
    for s in db.scalars(select(StudySession).order_by(StudySession.created_at.desc()).limit(limit)):
        mod = modules.get(s.module_key)
        if mod:
            note = f" · {s.note}" if s.note else ""
            items.append(Activity(as_utc(s.created_at), "study", f"Studied Module {mod.number} · {mod.title}",
                                  f"{s.minutes} min on {s.studied_on:%d %b}{note}", f"/modules/{mod.number}"))
    items.sort(key=lambda a: a.at, reverse=True)
    return items[:limit]


def active_days(db: Session) -> set[date]:
    days = set(db.scalars(select(StudySession.studied_on)))
    days |= {to_local(t).date() for t in db.scalars(select(StatusEvent.changed_at))}
    return days


# --- weekly study chart ---------------------------------------------------------

@dataclass
class Bar:
    week: date
    minutes: int
    x: float
    y: float
    height: float
    label: str


@dataclass
class WeekChart:
    bars: list[Bar]
    width: int
    height: int
    bar_width: float
    max_hours: int
    gridlines: list[tuple[float, str]] = field(default_factory=list)
    total_minutes: int = 0


def weekly_study_chart(db: Session, weeks: int = 8, today: date | None = None) -> WeekChart:
    """Minutes studied per week (Monday start) for the last `weeks` weeks, laid out for an inline SVG."""
    today = today or local_today()
    first = week_start(today) - timedelta(weeks=weeks - 1)
    per_week: Counter[date] = Counter()
    for studied_on, minutes in db.execute(select(StudySession.studied_on, StudySession.minutes)
                                          .where(StudySession.studied_on >= first)):
        per_week[week_start(studied_on)] += minutes

    width, height, top, bottom, left = 320, 150, 12, 22, 26
    plot_h = height - top - bottom
    slot = (width - left - 10) / weeks
    bar_w = slot * 0.56
    max_hours = max(1, math.ceil(max(per_week.values(), default=0) / 60))
    bars = []
    for i in range(weeks):
        wk = first + timedelta(weeks=i)
        minutes = per_week.get(wk, 0)
        h = plot_h * minutes / (max_hours * 60)
        bars.append(Bar(wk, minutes, left + i * slot + (slot - bar_w) / 2, top + plot_h - h, h,
                        "This wk" if i == weeks - 1 else f"{wk:%d/%m}"))
    gridlines = [(top + plot_h * (1 - f), f"{max_hours * f:g}h") for f in (0, 0.5, 1)]
    return WeekChart(bars, width, height, bar_w, max_hours, gridlines, sum(per_week.values()))


# --- per-episode and per-module stats ----------------------------------------

def production_minutes(t: ProductionTime | None) -> int:
    if t is None:
        return 0
    return (t.scripting_min or 0) + (t.prep_min or 0) + (t.editing_min or 0)


@dataclass
class Neighbours:
    prev: Episode | None
    next: Episode | None


def neighbours(db: Session, episode: Episode) -> Neighbours:
    base = select(Episode).where(Episode.version_id == episode.version_id)
    prev = db.scalar(base.where(Episode.position < episode.position).order_by(Episode.position.desc()).limit(1))
    nxt = db.scalar(base.where(Episode.position > episode.position).order_by(Episode.position).limit(1))
    return Neighbours(prev, nxt)


@dataclass
class ModuleStats:
    total: int
    published: int
    percent: int
    breakdown: list[tuple[str, str, int]]
    study_minutes: int
    production_minutes: int


def module_stats(db: Session, module: Module) -> ModuleStats:
    keys = [e.episode_key for e in module.episodes]
    statuses = list(db.scalars(select(EpisodeProgress.status).where(EpisodeProgress.episode_key.in_(keys))))
    counts = Counter(statuses)
    times = db.scalars(select(ProductionTime).where(ProductionTime.episode_key.in_(keys)))
    study = sum(db.scalars(select(StudySession.minutes).where(StudySession.module_key == module.module_key)))
    return ModuleStats(
        total=len(keys),
        published=counts["published"],
        percent=pct(counts["published"], len(keys)),
        breakdown=[(slug, label, counts[slug]) for slug, label in STATUSES],
        study_minutes=study,
        production_minutes=sum(production_minutes(t) for t in times),
    )
