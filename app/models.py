"""Database tables.

Course content (course_versions, modules, episodes) is read-only once imported.
Progress tables are keyed by episode_key / module_key, which stay the same across
course versions, so renumbering E012 in a later version never loses history.
"""

from datetime import date, datetime

from sqlalchemy import JSON, Boolean, Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.timeutil import utcnow

STATUSES: list[tuple[str, str]] = [
    ("not_started", "Not started"),
    ("scripted", "Scripted"),
    ("recorded", "Recorded"),
    ("edited", "Edited"),
    ("published", "Published"),
]
STATUS_LABELS = dict(STATUSES)


class Timestamped:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)


class User(Timestamped, Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    totp_secret: Mapped[str | None] = mapped_column(String(64))  # v1
    # Bumped on password change so every existing session cookie stops working.
    session_version: Mapped[int] = mapped_column(Integer, default=1)
    failed_login_count: Mapped[int] = mapped_column(Integer, default=0)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class CourseVersion(Timestamped, Base):
    __tablename__ = "course_versions"
    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(32))
    imported_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    source_markdown: Mapped[str] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)


class Module(Timestamped, Base):
    __tablename__ = "modules"
    __table_args__ = (UniqueConstraint("version_id", "number"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    version_id: Mapped[int] = mapped_column(ForeignKey("course_versions.id"))
    module_key: Mapped[str] = mapped_column(String(32), index=True)
    number: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(255))
    depth: Mapped[str] = mapped_column(String(64))
    learn: Mapped[str] = mapped_column(Text)
    build: Mapped[str] = mapped_column(Text)
    checkpoint: Mapped[str] = mapped_column(Text)
    lab_steps: Mapped[list] = mapped_column(JSON, default=list)
    lab_note: Mapped[str | None] = mapped_column(Text)

    episodes: Mapped[list["Episode"]] = relationship(back_populates="module", order_by="Episode.position")


class Episode(Timestamped, Base):
    __tablename__ = "episodes"
    __table_args__ = (UniqueConstraint("version_id", "code"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    version_id: Mapped[int] = mapped_column(ForeignKey("course_versions.id"))
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id"))
    episode_key: Mapped[str] = mapped_column(String(32), index=True)
    code: Mapped[str] = mapped_column(String(8))
    position: Mapped[int] = mapped_column(Integer)
    type: Mapped[str] = mapped_column(String(1))  # C or B
    title: Mapped[str] = mapped_column(String(255))
    hook: Mapped[str] = mapped_column(Text)
    claim: Mapped[str] = mapped_column(Text)
    show: Mapped[str] = mapped_column(Text)
    gotcha: Mapped[str] = mapped_column(Text)
    takeaway: Mapped[str] = mapped_column(Text)
    is_pilot: Mapped[bool] = mapped_column(Boolean, default=False)

    module: Mapped[Module] = relationship(back_populates="episodes")


class EpisodeProgress(Timestamped, Base):
    __tablename__ = "episode_progress"
    episode_key: Mapped[str] = mapped_column(String(32), primary_key=True)
    status: Mapped[str] = mapped_column(String(16), default="not_started")
    published_on: Mapped[date | None] = mapped_column(Date)
    video_url: Mapped[str | None] = mapped_column(String(500))
    final_length_seconds: Mapped[int | None] = mapped_column(Integer)
    script_markdown: Mapped[str | None] = mapped_column(Text)  # v1


class StatusEvent(Timestamped, Base):
    __tablename__ = "status_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    episode_key: Mapped[str] = mapped_column(String(32), index=True)
    from_status: Mapped[str] = mapped_column(String(16))
    to_status: Mapped[str] = mapped_column(String(16))
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class ProductionTime(Timestamped, Base):
    __tablename__ = "production_times"
    episode_key: Mapped[str] = mapped_column(String(32), primary_key=True)
    scripting_min: Mapped[int | None] = mapped_column(Integer)
    prep_min: Mapped[int | None] = mapped_column(Integer)
    takes: Mapped[int | None] = mapped_column(Integer)
    editing_min: Mapped[int | None] = mapped_column(Integer)


class ModuleProgress(Timestamped, Base):
    __tablename__ = "module_progress"
    module_key: Mapped[str] = mapped_column(String(32), primary_key=True)
    learned: Mapped[bool] = mapped_column(Boolean, default=False)
    built: Mapped[bool] = mapped_column(Boolean, default=False)
    tested: Mapped[bool] = mapped_column(Boolean, default=False)
    commit_sha: Mapped[str | None] = mapped_column(String(64))
    notes: Mapped[str | None] = mapped_column(Text)


class StudySession(Timestamped, Base):
    __tablename__ = "study_sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    module_key: Mapped[str] = mapped_column(String(32), index=True)
    studied_on: Mapped[date] = mapped_column(Date)
    minutes: Mapped[int] = mapped_column(Integer)
    note: Mapped[str | None] = mapped_column(String(500))


class EpisodeKeyMap(Timestamped, Base):
    """Written when a new course version is approved: which old episode each new one continues."""
    __tablename__ = "episode_key_map"
    id: Mapped[int] = mapped_column(primary_key=True)
    old_version_id: Mapped[int] = mapped_column(ForeignKey("course_versions.id"))
    old_code: Mapped[str] = mapped_column(String(8))
    new_version_id: Mapped[int] = mapped_column(ForeignKey("course_versions.id"))
    new_code: Mapped[str] = mapped_column(String(8))
    episode_key: Mapped[str] = mapped_column(String(32))
    approved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


# Order matters for export and for restoring from an export.
EXPORT_TABLES = [
    User, CourseVersion, Module, Episode, EpisodeProgress,
    StatusEvent, ProductionTime, ModuleProgress, StudySession, EpisodeKeyMap,
]
