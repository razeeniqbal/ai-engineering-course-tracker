import pytest
from sqlalchemy import func, select

from app.importer import SPEC_FIELDS, CourseImportError, import_course, parse_course
from app.models import Episode, EpisodeProgress, Module, ModuleProgress

MINI = """# Mini course

Version 3

## 6. Module map
| # | Module | Level | Episodes | Count |
|---|---|---|---|---:|
| 0 | Basics | Core | E001–E002 | 2 |

## 7. Modules and episodes

### Module 0 — Basics
**Depth:** Core
**Learn:** tokens.
**Build:** a client.
**Checkpoint:** a logged call.

**Lab steps**
1. Do one thing.
2. Do another.

Check your work.

**E001 · C · First episode** *(pilot)*
- Hook: Why?
- Claim: Because.
- Show: A diagram.
- Gotcha: A mistake.
- Takeaway: A lesson.

**E002 · B · Second episode**
- Hook: How?
- Claim: Like this, with a claim that
  wraps onto a second line.
- Show: Code.
- Gotcha: Another mistake.
- Takeaway: Another lesson.

## 8. Something else
**E999 · C · Not an episode**
"""


def test_v7_course_parses_16_modules_87_episodes(course_md):
    course = parse_course(course_md)
    assert course.label == "v7"
    assert len(course.modules) == 16
    assert [m.number for m in course.modules] == list(range(16))
    assert course.episode_count == 87
    codes = [e.code for m in course.modules for e in m.episodes]
    assert codes == [f"E{n:03d}" for n in range(1, 88)]
    for module in course.modules:
        for ep in module.episodes:
            assert all(ep.spec[f] for f in SPEC_FIELDS), ep.code
    pilots = sorted(e.code for m in course.modules for e in m.episodes if e.is_pilot)
    assert pilots == ["E001", "E012", "E014", "E037"]


def test_v7_module_fields_and_lab_steps(course_md):
    course = parse_course(course_md)
    m2 = course.modules[2]
    assert m2.title == "The application boundary and structured output"
    assert m2.fields["depth"] == "Core"
    assert m2.fields["build"].startswith("FastAPI service")
    m1 = course.modules[1]
    assert len(m1.lab_steps) == 5
    assert m1.lab_note.startswith("If the score looks suspiciously high")
    e012 = m2.episodes[0]
    assert (e012.code, e012.type, e012.title) == ("E012", "B", "Code calculates, the model explains")
    assert e012.spec["takeaway"] == "If it must be exact, compute it."


def test_mini_course_parsing():
    course = parse_course(MINI)
    assert course.label == "v3"
    (module,) = course.modules
    assert module.lab_steps == ["Do one thing.", "Do another."]
    assert module.lab_note == "Check your work."
    assert [e.code for e in module.episodes] == ["E001", "E002"]
    assert module.episodes[0].is_pilot and not module.episodes[1].is_pilot
    assert module.episodes[1].spec["claim"] == "Like this, with a claim that wraps onto a second line."


def test_missing_spec_field_is_reported():
    broken = MINI.replace("- Gotcha: Another mistake.\n", "")
    with pytest.raises(CourseImportError) as exc:
        parse_course(broken)
    assert "E002: missing Gotcha" in exc.value.errors


def test_module_map_mismatch_is_reported():
    broken = MINI.replace("| E001–E002 | 2 |", "| E001–E003 | 3 |")
    with pytest.raises(CourseImportError) as exc:
        parse_course(broken)
    assert any("module map says 3" in e for e in exc.value.errors)


def test_empty_file_is_rejected():
    with pytest.raises(CourseImportError):
        parse_course("# nothing here\n")


def test_import_creates_rows_with_stable_keys(db, course_md):
    version = import_course(db, course_md)
    assert version.label == "v7" and version.is_active
    assert db.scalar(select(func.count()).select_from(Module)) == 16
    assert db.scalar(select(func.count()).select_from(Episode)) == 87
    assert db.scalar(select(func.count()).select_from(EpisodeProgress)) == 87
    assert db.scalar(select(func.count()).select_from(ModuleProgress)) == 16
    keys = db.scalars(select(Episode.episode_key)).all()
    assert len(set(keys)) == 87 and all(k.startswith("ep_") for k in keys)
    statuses = set(db.scalars(select(EpisodeProgress.status)))
    assert statuses == {"not_started"}


def test_second_import_is_refused(db, course_md):
    import_course(db, course_md)
    with pytest.raises(CourseImportError, match="already loaded"):
        import_course(db, course_md)


def test_upload_through_settings(authed, db, course_md):
    r = authed.post("/settings/import", files={"course_file": ("course.md", course_md.encode(), "text/markdown")},
                    data={"label": ""})
    assert r.status_code == 303
    assert db.scalar(select(func.count()).select_from(Episode)) == 87
    page = authed.get("/settings").text
    assert "v7" in page


def test_upload_with_errors_shows_them(authed, db):
    r = authed.post("/settings/import", files={"course_file": ("c.md", MINI.replace("- Hook: Why?\n", "").encode())})
    assert r.status_code == 422 and "E001: missing Hook" in r.text
    assert db.scalar(select(func.count()).select_from(Episode)) == 0
