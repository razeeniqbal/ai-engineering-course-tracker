"""Parse the course markdown into modules and episodes, and load it into the database.

Expected shape (see course/AI_Engineering_Course_Razeen_v7.md, Section 7):

    ### Module 2 — The application boundary and structured output
    **Depth:** Core
    **Learn:** ...
    **Build:** ...
    **Checkpoint:** ...

    **Lab steps**            (optional)
    1. ...

    **E012 · B · Code calculates, the model explains** *(pilot, ...)*
    - Hook: ...
    - Claim: ...
    - Show: ...
    - Gotcha: ...
    - Takeaway: ...
"""

import re
import uuid
from dataclasses import dataclass, field

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import CourseVersion, Episode, EpisodeProgress, Module, ModuleProgress

SPEC_FIELDS = ("hook", "claim", "show", "gotcha", "takeaway")
MODULE_FIELDS = ("depth", "learn", "build", "checkpoint")

MODULE_RE = re.compile(r"^###\s+Module\s+(\d+)\s+[—–-]\s+(.+?)\s*$")
EPISODE_RE = re.compile(r"^\*\*(E\d{3})\s+·\s+([CB])\s+·\s+(.+?)\*\*\s*(?:\*\((.+?)\)\*)?\s*$")
MODULE_FIELD_RE = re.compile(r"^\*\*(Depth|Learn|Build|Checkpoint):\*\*\s*(.*)$")
SPEC_RE = re.compile(r"^-\s+(Hook|Claim|Show|Gotcha|Takeaway):\s*(.*)$")
LAB_HEADING_RE = re.compile(r"^\*\*Lab steps\*\*\s*$")
LAB_STEP_RE = re.compile(r"^\d+\.\s+(.*)$")
MAP_ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|.*\|\s*(\d+)\s*\|\s*$")
VERSION_RE = re.compile(r"^Version\s+(\d+)\b", re.MULTILINE)


class CourseImportError(ValueError):
    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__("; ".join(errors))


@dataclass
class ParsedEpisode:
    code: str
    type: str
    title: str
    is_pilot: bool
    spec: dict[str, str] = field(default_factory=dict)


@dataclass
class ParsedModule:
    number: int
    title: str
    fields: dict[str, str] = field(default_factory=dict)
    lab_steps: list[str] = field(default_factory=list)
    lab_note: str | None = None
    episodes: list[ParsedEpisode] = field(default_factory=list)


@dataclass
class ParsedCourse:
    label: str | None
    modules: list[ParsedModule]

    @property
    def episode_count(self) -> int:
        return sum(len(m.episodes) for m in self.modules)


def _module_map_counts(lines: list[str]) -> dict[int, int]:
    """Episode counts per module from the Section 6 table, if present."""
    counts: dict[int, int] = {}
    in_map = False
    for line in lines:
        if line.startswith("## "):
            in_map = "Module map" in line
            continue
        if in_map and (m := MAP_ROW_RE.match(line)):
            counts[int(m.group(1))] = int(m.group(2))
    return counts


def parse_course(markdown: str) -> ParsedCourse:
    lines = markdown.replace("\r\n", "\n").split("\n")
    modules: list[ParsedModule] = []
    module: ParsedModule | None = None
    episode: ParsedEpisode | None = None
    in_lab = False
    lab_note: list[str] = []
    last_key: tuple[object, str] | None = None  # where a continuation line should go

    def close_lab() -> None:
        nonlocal in_lab, lab_note
        if module is not None and lab_note:
            module.lab_note = " ".join(lab_note)
        in_lab, lab_note = False, []

    for line in lines:
        stripped = line.strip()
        if line.startswith("## ") or (line.startswith("### ") and not MODULE_RE.match(line)):
            # Any other section heading ends module parsing.
            close_lab()
            module, episode, last_key = None, None, None
            continue
        if m := MODULE_RE.match(line):
            close_lab()
            module = ParsedModule(number=int(m.group(1)), title=m.group(2))
            modules.append(module)
            episode, last_key = None, None
            continue
        if module is None:
            continue
        if m := EPISODE_RE.match(stripped):
            close_lab()
            note = (m.group(4) or "").lower()
            episode = ParsedEpisode(code=m.group(1), type=m.group(2), title=m.group(3).strip(),
                                    is_pilot="pilot" in note)
            module.episodes.append(episode)
            last_key = None
            continue
        if episode is not None and (m := SPEC_RE.match(stripped)):
            key = m.group(1).lower()
            episode.spec[key] = m.group(2).strip()
            last_key = (episode, key)
            continue
        if episode is None and (m := MODULE_FIELD_RE.match(stripped)):
            key = m.group(1).lower()
            module.fields[key] = m.group(2).strip()
            last_key = (module, key)
            continue
        if episode is None and LAB_HEADING_RE.match(stripped):
            in_lab, last_key = True, None
            continue
        if in_lab:
            if m := LAB_STEP_RE.match(stripped):
                module.lab_steps.append(m.group(1).strip())
            elif stripped:
                lab_note.append(stripped)
            continue
        if not stripped:
            last_key = None
            continue
        if last_key is not None and not stripped.startswith(("-", "**", "|")):
            # Wrapped continuation of the previous field.
            target, key = last_key
            store = target.spec if isinstance(target, ParsedEpisode) else target.fields
            store[key] = f"{store[key]} {stripped}".strip()
    close_lab()

    label_match = VERSION_RE.search(markdown)
    course = ParsedCourse(label=f"v{label_match.group(1)}" if label_match else None, modules=modules)
    validate_course(course, _module_map_counts(lines))
    return course


def validate_course(course: ParsedCourse, expected_counts: dict[int, int] | None = None) -> None:
    errors: list[str] = []
    if not course.modules:
        errors.append("No modules found (expected headings like '### Module 0 — Title')")
    seen_numbers: set[int] = set()
    seen_codes: set[str] = set()
    for mod in course.modules:
        if mod.number in seen_numbers:
            errors.append(f"Module {mod.number} appears twice")
        seen_numbers.add(mod.number)
        for f in MODULE_FIELDS:
            if not mod.fields.get(f):
                errors.append(f"Module {mod.number}: missing {f.capitalize()}")
        if not mod.episodes:
            errors.append(f"Module {mod.number}: no episodes")
        for ep in mod.episodes:
            if ep.code in seen_codes:
                errors.append(f"{ep.code} appears twice")
            seen_codes.add(ep.code)
            missing = [f.capitalize() for f in SPEC_FIELDS if not ep.spec.get(f)]
            if missing:
                errors.append(f"{ep.code}: missing {', '.join(missing)}")
        if expected_counts and mod.number in expected_counts and expected_counts[mod.number] != len(mod.episodes):
            errors.append(f"Module {mod.number}: module map says {expected_counts[mod.number]} episodes, "
                          f"found {len(mod.episodes)}")
    if errors:
        raise CourseImportError(errors)


def new_key(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:16]}"


def active_version(db: Session) -> CourseVersion | None:
    # Cached on the session: one page asks for it several times, and a session lives for one request.
    if "active_version" not in db.info:
        version = db.scalar(select(CourseVersion).where(CourseVersion.is_active.is_(True)))
        if version is None:
            return None
        db.info["active_version"] = version
    return db.info["active_version"]


def import_course(db: Session, markdown: str, label: str | None = None) -> CourseVersion:
    """First import only. Importing a new version over existing progress is a v1 feature."""
    if active_version(db) is not None:
        raise CourseImportError(["A course version is already loaded. Version upgrades arrive in v1."])
    parsed = parse_course(markdown)
    version = CourseVersion(label=(label or parsed.label or "v?").strip(), source_markdown=markdown,
                            is_active=True)
    db.add(version)
    db.flush()
    position = 0
    for pm in parsed.modules:
        module = Module(version_id=version.id, module_key=new_key("mod"), number=pm.number, title=pm.title,
                        lab_steps=pm.lab_steps, lab_note=pm.lab_note, **pm.fields)
        db.add(module)
        db.flush()
        db.add(ModuleProgress(module_key=module.module_key))
        for pe in pm.episodes:
            position += 1
            ep = Episode(version_id=version.id, module_id=module.id, episode_key=new_key("ep"), code=pe.code,
                         position=position, type=pe.type, title=pe.title, is_pilot=pe.is_pilot, **pe.spec)
            db.add(ep)
            db.add(EpisodeProgress(episode_key=ep.episode_key))
    db.commit()
    db.info["active_version"] = version
    return version
