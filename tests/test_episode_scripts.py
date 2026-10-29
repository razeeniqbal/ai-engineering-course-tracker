import re

import pytest

from app.importer import import_course, parse_course
from app.models import EpisodeProgress
from app.scripts import load_scripts, read_script_files, stats
from tests.conftest import ROOT

SCRIPTS_DIR = ROOT / "course" / "scripts"
V8_PATH = ROOT / "course" / "AI_Engineering_Course_Razeen_v8.md"
SECTIONS = ("Hook", "Claim", "Show", "Gotcha", "Takeaway")


@pytest.fixture(scope="module")
def v8():
    return parse_course(V8_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def scripts():
    return read_script_files(SCRIPTS_DIR)


def test_every_v8_episode_has_exactly_one_script(v8, scripts):
    assert set(scripts) == {e.code for m in v8.modules for e in m.episodes}


def test_script_headings_match_the_course(v8):
    titles = {e.code: (e.type, e.title) for m in v8.modules for e in m.episodes}
    for path in SCRIPTS_DIR.glob("module-*.md"):
        for code, typ, title in re.findall(r"^## (E\d{3}) · ([CB]) · (.+)$", path.read_text(encoding="utf-8"), re.M):
            assert (typ, title) == titles[code], code


def test_scripts_have_all_five_sections_and_fit_two_minutes(v8, scripts):
    types = {e.code: e.type for m in v8.modules for e in m.episodes}
    for code, body in scripts.items():
        for section in SECTIONS:
            assert re.search(rf"^\*\*\d:\d\d–\d:\d\d · {section}\*\*$", body, re.M), f"{code} lacks {section}"
        s = stats(body, types[code])
        assert s.spoken_only and s.verdict == "on-target", f"{code}: {s.words} words ({s.low}-{s.high})"


def test_day_one_script_is_not_loaded_as_an_episode(scripts):
    assert (SCRIPTS_DIR / "day-001.md").exists()
    assert all(code.startswith("E") for code in scripts)


def test_load_fills_empty_scripts_and_keeps_edited_ones(db, scripts):
    import_course(db, V8_PATH.read_text(encoding="utf-8"))
    first = load_scripts(db, scripts)
    assert len(first.filled) == 87 and not first.skipped and not first.unknown

    e012 = next(p for p in db.query(EpisodeProgress) if p.script_markdown and "service_revenue" in p.script_markdown)
    e012.script_markdown = "> my own version"
    db.commit()

    second = load_scripts(db, scripts)
    assert second.filled == [] and len(second.skipped) == 87
    db.refresh(e012)
    assert e012.script_markdown == "> my own version"

    third = load_scripts(db, scripts, overwrite=True)
    assert len(third.filled) == 87
    db.refresh(e012)
    assert "service_revenue" in e012.script_markdown


def test_unknown_codes_are_reported(db):
    import_course(db, V8_PATH.read_text(encoding="utf-8"))
    result = load_scripts(db, {"E999": "> nope"})
    assert result.unknown == ["E999"] and result.filled == []
