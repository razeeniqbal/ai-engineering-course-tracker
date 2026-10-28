import json
import re

import pytest
from sqlalchemy import func, select

from app.importer import NEW, CourseImportError, active_version, apply_upgrade, import_course, plan_upgrade, parse_course
from app.models import (
    CourseVersion, Episode, EpisodeKeyMap, EpisodeProgress, ModuleProgress, ProductionTime, StatusEvent, StudySession,
)
from tests.conftest import ROOT
from tests.test_import import MINI

V8_PATH = ROOT / "course" / "AI_Engineering_Course_Razeen_v8.md"


@pytest.fixture
def v8_md() -> str:
    return V8_PATH.read_text(encoding="utf-8")


def _ep(db, code: str) -> Episode:
    version = active_version(db)
    return db.scalar(select(Episode).where(Episode.version_id == version.id, Episode.code == code))


def test_v8_course_parses_like_v7(course_md, v8_md):
    v7, v8 = parse_course(course_md), parse_course(v8_md)
    assert v8.label == "v8" and len(v8.modules) == 16 and v8.episode_count == 87
    old = {e.code: (m.number, e.type) for m in v7.modules for e in m.episodes}
    new = {e.code: (m.number, e.type) for m in v8.modules for e in m.episodes}
    assert old == new  # same code, module and type for every episode, so progress lines up by code
    assert sorted(e.code for m in v8.modules for e in m.episodes if e.is_pilot) == ["E001", "E012", "E014", "E037"]
    e012 = next(e for e in v8.modules[2].episodes if e.code == "E012")
    assert e012.title == "Should AI add up your service revenue?"
    assert "Dealer A" in e012.spec["show"]


def test_plan_matches_every_v7_episode_by_code(db, course, v8_md):
    plan = plan_upgrade(db, v8_md)
    assert plan.label == "v8"
    assert plan.count("code") == 87 and not plan.unmatched and not plan.removed
    assert len(plan.renamed) >= 80
    assert plan.new_modules == [] and plan.removed_modules == []


def test_upgrade_keeps_every_kind_of_progress(authed, course, db, v8_md):
    e012 = _ep(db, "E012")
    key = e012.episode_key
    authed.post(f"/episodes/{key}/status", data={"status": "scripted"}, htmx=True)
    authed.post(f"/episodes/{key}/script", data={"script_markdown": "> my draft"}, htmx=True)
    authed.post(f"/episodes/{key}/production", data={"scripting_min": "45"}, htmx=True)
    authed.post("/modules/2/check", data={"field": "learned", "checked": "on"}, htmx=True)
    authed.post("/study", data={"module_number": "2", "minutes": "30"}, htmx=True)
    module_key = db.scalar(select(ModuleProgress.module_key).where(ModuleProgress.learned.is_(True)))

    version = apply_upgrade(db, v8_md)
    db.expire_all()

    assert version.label == "v8" and version.is_active
    assert db.scalar(select(func.count()).select_from(CourseVersion).where(CourseVersion.is_active.is_(True))) == 1
    new_e012 = _ep(db, "E012")
    assert new_e012.episode_key == key and new_e012.title == "Should AI add up your service revenue?"
    progress = db.get(EpisodeProgress, key)
    assert (progress.status, progress.script_markdown) == ("scripted", "> my draft")
    assert db.get(ProductionTime, key).scripting_min == 45
    assert db.scalar(select(func.count()).select_from(StatusEvent).where(StatusEvent.episode_key == key)) == 1
    assert db.get(ModuleProgress, module_key).learned is True
    assert db.scalar(select(StudySession.module_key)) == module_key
    assert db.scalar(select(func.count()).select_from(EpisodeKeyMap)) == 87
    assert db.scalar(select(func.count()).select_from(EpisodeProgress)) == 87  # nothing duplicated

    page = authed.get(f"/episodes/{key}").text
    assert "Should AI add up your service revenue?" in page and "my draft" in page


def test_title_matching_and_hand_picked_matches(db):
    v1 = MINI
    import_course(db, v1)
    old_e002 = _ep(db, "E002").episode_key
    # E002 renumbered to E003 with the same title; E001 replaced by a new E009 the user says continues it.
    v2 = (MINI.replace("Version 3", "Version 4")
              .replace("**E002 · B · Second episode**", "**E003 · B · Second episode**")
              .replace("**E001 · C · First episode** *(pilot)*", "**E009 · C · Brand new first** *(pilot)*")
              .replace("| E001–E002 | 2 |", "| E003–E009 | 2 |"))
    plan = plan_upgrade(db, v2)
    by_code = {m.new.code: m for m in plan.matches}
    assert by_code["E003"].how == "title" and by_code["E003"].old.code == "E002"
    assert by_code["E009"].old is None and [e.code for e in plan.removed] == ["E001"]

    plan = plan_upgrade(db, v2, overrides={"E009": "E001"})
    assert {m.new.code: m.how for m in plan.matches} == {"E009": "manual", "E003": "title"}
    assert plan.removed == []

    apply_upgrade(db, v2, overrides={"E009": "E001"})
    assert _ep(db, "E003").episode_key == old_e002


def test_new_episode_override_and_bad_inputs(db, course, v8_md):
    plan = plan_upgrade(db, v8_md, overrides={"E005": NEW})
    assert [m.new.code for m in plan.unmatched] == ["E005"] and [e.code for e in plan.removed] == ["E005"]
    with pytest.raises(CourseImportError, match="no E999"):
        plan_upgrade(db, v8_md, overrides={"E001": "E999"})
    with pytest.raises(CourseImportError, match="more than one"):
        plan_upgrade(db, v8_md, overrides={"E001": "E002", "E003": "E002"})
    with pytest.raises(CourseImportError, match="already loaded"):
        plan_upgrade(db, v8_md, label="v7")


def test_upgrade_through_settings_pages(authed, course, db, v8_md):
    e001 = _ep(db, "E001").episode_key
    authed.post(f"/episodes/{e001}/status", data={"status": "recorded"}, htmx=True)
    r = authed.post("/settings/upgrade/preview", files={"course_file": ("v8.md", v8_md.encode(), "text/markdown")})
    assert r.status_code == 200
    assert "v7 → v8" in r.text and "Approve and switch to v8" in r.text
    assert re.search(r"<b>1</b> episode with progress", r.text)
    markdown = re.search(r'<textarea name="markdown" hidden aria-hidden="true">(.*?)</textarea>', r.text, re.S).group(1)

    r = authed.post("/settings/upgrade/apply", data={"markdown": _unescape(markdown), "label": "v8"})
    assert r.status_code == 303 and "Now+on+course+v8" in r.headers["location"]
    db.expire_all()
    db.info.pop("active_version", None)  # this test session cached v7 before the app switched versions
    assert active_version(db).label == "v8"
    assert db.get(EpisodeProgress, e001).status == "recorded"
    assert "Why AI demos break in real life" in authed.get("/episodes").text

    data = json.loads(authed.get("/export/json").text)["tables"]
    assert len(data["course_versions"]) == 2 and len(data["episode_key_map"]) == 87


def test_preview_errors_are_shown(authed, course):
    r = authed.post("/settings/upgrade/preview", files={"course_file": ("bad.md", b"# nothing", "text/markdown")})
    assert r.status_code == 422 and "Couldn't prepare the upgrade" in r.text


def _unescape(html: str) -> str:
    import html as html_lib
    return html_lib.unescape(html)
