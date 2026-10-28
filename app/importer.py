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

from app.models import CourseVersion, Episode, EpisodeKeyMap, EpisodeProgress, Module, ModuleProgress

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
    """First import only. Later versions go through plan_upgrade / apply_upgrade."""
    if active_version(db) is not None:
        raise CourseImportError(["A course version is already loaded. Upload a new version to upgrade."])
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


# --- upgrading to a new course version ------------------------------------------
# Progress lives on episode_key / module_key, so an upgrade only has to decide which old
# episode each new one continues; the new rows reuse that key and every status, script,
# time and history entry carries over untouched.

NEW = "new"


@dataclass
class EpisodeMatch:
    new: ParsedEpisode
    module_number: int
    old: Episode | None
    how: str  # "code", "title", "manual" or "new"

    @property
    def title_changed(self) -> bool:
        return self.old is not None and self.old.title != self.new.title


@dataclass
class UpgradePlan:
    label: str
    current: CourseVersion
    matches: list[EpisodeMatch]
    removed: list[Episode]
    new_modules: list[int]
    removed_modules: list[int]

    @property
    def unmatched(self) -> list[EpisodeMatch]:
        return [m for m in self.matches if m.old is None]

    @property
    def renamed(self) -> list[EpisodeMatch]:
        return [m for m in self.matches if m.title_changed]

    def count(self, how: str) -> int:
        return sum(m.how == how for m in self.matches)


def _norm(title: str) -> str:
    return re.sub(r"\s+", " ", title).strip().lower()


def plan_upgrade(db: Session, markdown: str, label: str | None = None,
                 overrides: dict[str, str] | None = None) -> UpgradePlan:
    """Match each new episode to an old one: hand-picked first, then same code, then same title.

    `overrides` maps a new episode code to an old code, or to NEW to start it fresh.
    """
    current = active_version(db)
    if current is None:
        raise CourseImportError(["No course is loaded yet; import it first."])
    parsed = parse_course(markdown)
    new_label = (label or parsed.label or "").strip()
    if not new_label:
        raise CourseImportError(["Give the new version a label, e.g. v8."])
    if new_label == current.label:
        raise CourseImportError([f"{new_label} is already loaded. Use a different label for the new version."])

    old_eps = list(db.scalars(select(Episode).where(Episode.version_id == current.id).order_by(Episode.position)))
    by_code = {e.code: e for e in old_eps}
    overrides = {k: v for k, v in (overrides or {}).items() if v}
    errors = [f"{new} → {old}: there is no {old} in {current.label}"
              for new, old in overrides.items() if old != NEW and old not in by_code]
    if errors:
        raise CourseImportError(errors)

    pairs = [(pm.number, pe) for pm in parsed.modules for pe in pm.episodes]
    claimed: set[str] = set()
    chosen: dict[str, tuple[Episode | None, str]] = {}
    for _, pe in pairs:  # 1. choices made by hand
        old_code = overrides.get(pe.code)
        if old_code == NEW:
            chosen[pe.code] = (None, "new")
        elif old_code:
            if old_code in claimed:
                raise CourseImportError([f"{old_code} is picked for more than one new episode."])
            claimed.add(old_code)
            chosen[pe.code] = (by_code[old_code], "manual")
    for _, pe in pairs:  # 2. same code
        if pe.code not in chosen and pe.code in by_code and pe.code not in claimed:
            claimed.add(pe.code)
            chosen[pe.code] = (by_code[pe.code], "code")
    by_title = {}
    for e in old_eps:
        if e.code not in claimed:
            by_title.setdefault(_norm(e.title), e)
    for _, pe in pairs:  # 3. same title among the old episodes nobody has claimed
        if pe.code not in chosen:
            old = by_title.pop(_norm(pe.title), None)
            if old is not None and old.code not in claimed:
                claimed.add(old.code)
                chosen[pe.code] = (old, "title")
            else:
                chosen[pe.code] = (None, "new")

    old_module_numbers = set(db.scalars(select(Module.number).where(Module.version_id == current.id)))
    new_module_numbers = {pm.number for pm in parsed.modules}
    return UpgradePlan(
        label=new_label,
        current=current,
        matches=[EpisodeMatch(pe, number, *chosen[pe.code]) for number, pe in pairs],
        removed=[e for e in old_eps if e.code not in claimed],
        new_modules=sorted(new_module_numbers - old_module_numbers),
        removed_modules=sorted(old_module_numbers - new_module_numbers),
    )


def apply_upgrade(db: Session, markdown: str, label: str | None = None,
                  overrides: dict[str, str] | None = None) -> CourseVersion:
    """Load the new version as the active one; the old version stays in the database, read-only."""
    plan = plan_upgrade(db, markdown, label, overrides)
    parsed = parse_course(markdown)
    old_modules = {m.number: m for m in db.scalars(select(Module).where(Module.version_id == plan.current.id))}
    match_for = {m.new.code: m for m in plan.matches}

    plan.current.is_active = False
    version = CourseVersion(label=plan.label, source_markdown=markdown, is_active=True)
    db.add(version)
    db.flush()
    position = 0
    for pm in parsed.modules:
        old_module = old_modules.get(pm.number)
        module_key = old_module.module_key if old_module else new_key("mod")
        module = Module(version_id=version.id, module_key=module_key, number=pm.number, title=pm.title,
                        lab_steps=pm.lab_steps, lab_note=pm.lab_note, **pm.fields)
        db.add(module)
        db.flush()
        if old_module is None:
            db.add(ModuleProgress(module_key=module_key))
        for pe in pm.episodes:
            position += 1
            match = match_for[pe.code]
            key = match.old.episode_key if match.old else new_key("ep")
            db.add(Episode(version_id=version.id, module_id=module.id, episode_key=key, code=pe.code,
                           position=position, type=pe.type, title=pe.title, is_pilot=pe.is_pilot, **pe.spec))
            if match.old is None:
                db.add(EpisodeProgress(episode_key=key))
            else:
                db.add(EpisodeKeyMap(old_version_id=plan.current.id, old_code=match.old.code,
                                     new_version_id=version.id, new_code=pe.code, episode_key=key))
    db.commit()
    db.info["active_version"] = version
    return version
