"""Queries and updates shared by the pages."""

from collections import Counter
from dataclasses import dataclass
from datetime import date, timedelta

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, joinedload

from app import insights
from app.importer import active_version
from app.models import (
    STATUS_LABELS, STATUSES, Episode, EpisodeProgress, Module, ModuleProgress, ProductionTime,
    StatusEvent, StudySession,
)
from app.timeutil import local_today, utcnow, week_start


class NotFound(Exception):
    pass


@dataclass
class EpisodeRow:
    episode: Episode
    progress: EpisodeProgress

    @property
    def status_label(self) -> str:
        return STATUS_LABELS[self.progress.status]


def episode_rows(db: Session, module_number: int | None = None, status: str | None = None,
                 type_: str | None = None, q: str | None = None) -> list[EpisodeRow]:
    version = active_version(db)
    if version is None:
        return []
    stmt = (select(Episode, EpisodeProgress)
            .join(EpisodeProgress, EpisodeProgress.episode_key == Episode.episode_key)
            .join(Module, Module.id == Episode.module_id)
            .where(Episode.version_id == version.id)
            .options(joinedload(Episode.module))
            .order_by(Episode.position))
    if module_number is not None:
        stmt = stmt.where(Module.number == module_number)
    if status:
        stmt = stmt.where(EpisodeProgress.status == status)
    if type_:
        stmt = stmt.where(Episode.type == type_)
    if q:
        like = f"%{q.strip()}%"
        stmt = stmt.where(or_(Episode.code.ilike(like), Episode.title.ilike(like), Episode.claim.ilike(like),
                              Episode.hook.ilike(like)))
    return [EpisodeRow(e, p) for e, p in db.execute(stmt).all()]


def get_episode(db: Session, episode_key: str) -> EpisodeRow:
    version = active_version(db)
    row = db.execute(
        select(Episode, EpisodeProgress)
        .join(EpisodeProgress, EpisodeProgress.episode_key == Episode.episode_key)
        .where(Episode.episode_key == episode_key, Episode.version_id == (version.id if version else -1))
        .options(joinedload(Episode.module))
    ).first()
    if row is None:
        raise NotFound(episode_key)
    return EpisodeRow(*row)


def needs_publish_details(progress: EpisodeProgress) -> bool:
    return not (progress.video_url and progress.final_length_seconds)


def change_status(db: Session, episode_key: str, new_status: str) -> StatusEvent | None:
    if new_status not in STATUS_LABELS:
        raise ValueError(f"Unknown status {new_status!r}")
    progress = db.get(EpisodeProgress, episode_key)
    if progress is None:
        raise NotFound(episode_key)
    if progress.status == new_status:
        return None
    event = StatusEvent(episode_key=episode_key, from_status=progress.status, to_status=new_status,
                        changed_at=utcnow())
    progress.status = new_status
    db.add(event)
    db.commit()
    return event


def publish(db: Session, episode_key: str, video_url: str, length_seconds: int, published_on: date) -> None:
    progress = db.get(EpisodeProgress, episode_key)
    if progress is None:
        raise NotFound(episode_key)
    progress.video_url = video_url
    progress.final_length_seconds = length_seconds
    progress.published_on = published_on
    db.commit()
    change_status(db, episode_key, "published")


def save_script(db: Session, episode_key: str, markdown: str) -> None:
    progress = db.get(EpisodeProgress, episode_key)
    if progress is None:
        raise NotFound(episode_key)
    # Normalise Windows line endings so word counts and diffs stay stable.
    progress.script_markdown = markdown.replace("\r\n", "\n").strip("\n") or None
    db.commit()


def status_history(db: Session, episode_key: str) -> list[StatusEvent]:
    return list(db.scalars(select(StatusEvent).where(StatusEvent.episode_key == episode_key)
                           .order_by(StatusEvent.changed_at.desc(), StatusEvent.id.desc())))


def production_time(db: Session, episode_key: str) -> ProductionTime:
    return db.get(ProductionTime, episode_key) or ProductionTime(episode_key=episode_key)


def save_production_time(db: Session, episode_key: str, **values: int | None) -> None:
    row = db.get(ProductionTime, episode_key)
    if row is None:
        row = ProductionTime(episode_key=episode_key)
        db.add(row)
    for name, value in values.items():
        setattr(row, name, value)
    db.commit()


# --- modules ------------------------------------------------------------------

@dataclass
class ModuleRow:
    module: Module
    progress: ModuleProgress
    published: int
    total: int
    study_minutes: int


def module_rows(db: Session) -> list[ModuleRow]:
    version = active_version(db)
    if version is None:
        return []
    modules = db.scalars(select(Module).where(Module.version_id == version.id).order_by(Module.number)
                         .options(joinedload(Module.episodes))).unique().all()
    progress = {p.module_key: p for p in db.scalars(select(ModuleProgress))}
    published = Counter(
        mid for mid, in db.execute(
            select(Episode.module_id)
            .join(EpisodeProgress, EpisodeProgress.episode_key == Episode.episode_key)
            .where(Episode.version_id == version.id, EpisodeProgress.status == "published")))
    minutes = dict(db.execute(select(StudySession.module_key, func.sum(StudySession.minutes))
                              .group_by(StudySession.module_key)).all())
    return [ModuleRow(m, progress.get(m.module_key) or ModuleProgress(module_key=m.module_key),
                      published[m.id], len(m.episodes), int(minutes.get(m.module_key) or 0))
            for m in modules]


def get_module(db: Session, number: int) -> Module:
    version = active_version(db)
    module = db.scalar(select(Module).where(Module.version_id == (version.id if version else -1),
                                            Module.number == number))
    if module is None:
        raise NotFound(str(number))
    return module


def module_progress(db: Session, module_key: str) -> ModuleProgress:
    row = db.get(ModuleProgress, module_key)
    if row is None:
        row = ModuleProgress(module_key=module_key)
        db.add(row)
        db.commit()
    return row


def study_sessions(db: Session, module_key: str | None = None, limit: int = 50) -> list[StudySession]:
    stmt = select(StudySession).order_by(StudySession.studied_on.desc(), StudySession.id.desc()).limit(limit)
    if module_key:
        stmt = stmt.where(StudySession.module_key == module_key)
    return list(db.scalars(stmt))


def add_study_session(db: Session, module_key: str, studied_on: date, minutes: int, note: str | None) -> None:
    if minutes <= 0 or minutes > 24 * 60:
        raise ValueError("Minutes must be between 1 and 1440")
    db.add(StudySession(module_key=module_key, studied_on=studied_on, minutes=minutes,
                        note=(note or "").strip()[:500] or None))
    db.commit()


# --- dashboard ----------------------------------------------------------------

@dataclass
class Dashboard:
    has_course: bool
    total: int
    by_status: list[tuple[str, str, int]]
    up_next: list[EpisodeRow]
    modules: list[ModuleRow]
    study_minutes_week: int
    week_start: date
    rings: list[insights.Ring]
    pace: insights.Pace
    streak: int
    activity: list[insights.Activity]
    chart: insights.WeekChart


def dashboard(db: Session) -> Dashboard:
    rows = episode_rows(db)
    counts = Counter(r.progress.status for r in rows)
    start = week_start(local_today())
    week_minutes = db.scalar(select(func.coalesce(func.sum(StudySession.minutes), 0))
                             .where(StudySession.studied_on >= start,
                                    StudySession.studied_on < start + timedelta(days=7))) or 0
    # Work already in progress comes before untouched episodes, each in course order.
    pending = [r for r in rows if r.progress.status != "published"]
    pending.sort(key=lambda r: (r.progress.status == "not_started", r.episode.position))
    modules = module_rows(db)
    published_dates = [r.progress.published_on for r in rows
                       if r.progress.status == "published" and r.progress.published_on]
    return Dashboard(
        has_course=bool(rows),
        total=len(rows),
        by_status=[(slug, label, counts[slug]) for slug, label in STATUSES],
        up_next=pending[:5],
        modules=modules,
        study_minutes_week=int(week_minutes),
        week_start=start,
        rings=insights.rings([r.progress.status for r in rows], [m.progress for m in modules], len(modules)),
        pace=insights.pace(published_dates, len(pending)),
        streak=insights.streak(insights.active_days(db)),
        activity=insights.activity(db),
        chart=insights.weekly_study_chart(db),
    )
