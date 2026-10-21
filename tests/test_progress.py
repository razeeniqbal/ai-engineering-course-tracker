from datetime import timedelta

import pytest
from sqlalchemy import select

from app import services
from app.models import Episode, EpisodeProgress, ModuleProgress, ProductionTime, StatusEvent, StudySession
from app.timeutil import format_length, local_today, parse_length, week_start


def _episode(db, code: str) -> Episode:
    return db.scalar(select(Episode).where(Episode.code == code))


def test_status_change_records_dated_history(authed, course, db):
    ep = _episode(db, "E001")
    r = authed.post(f"/episodes/{ep.episode_key}/status", data={"status": "scripted"}, htmx=True)
    assert r.status_code == 200 and r.headers["HX-Trigger"] == "statusChanged"
    assert 'value="scripted" selected' in r.text
    authed.post(f"/episodes/{ep.episode_key}/status", data={"status": "recorded"}, htmx=True)

    events = db.scalars(select(StatusEvent).where(StatusEvent.episode_key == ep.episode_key)
                        .order_by(StatusEvent.id)).all()
    assert [(e.from_status, e.to_status) for e in events] == [("not_started", "scripted"), ("scripted", "recorded")]
    assert all(e.changed_at is not None for e in events)
    db.expire_all()
    assert db.get(EpisodeProgress, ep.episode_key).status == "recorded"

    page = authed.get(f"/episodes/{ep.episode_key}").text
    assert "from Scripted" in page and "Production stage" in page


def test_dashboard_counts_update(authed, course, db):
    ep = _episode(db, "E005")
    before = services.dashboard(db)
    assert dict((s, c) for s, _, c in before.by_status)["not_started"] == 87
    authed.post(f"/episodes/{ep.episode_key}/status", data={"status": "edited"}, htmx=True)
    summary = authed.get("/dashboard/summary").text
    db.expire_all()
    after = dict((s, c) for s, _, c in services.dashboard(db).by_status)
    assert after["not_started"] == 86 and after["edited"] == 1
    # Work in progress jumps to the top of "Up next".
    assert services.dashboard(db).up_next[0].episode.code == "E005"
    assert "E005" in summary


def test_same_status_adds_no_event(authed, course, db):
    ep = _episode(db, "E002")
    authed.post(f"/episodes/{ep.episode_key}/status", data={"status": "not_started"}, htmx=True)
    assert db.scalars(select(StatusEvent)).all() == []


def test_unknown_status_rejected(authed, course, db):
    ep = _episode(db, "E002")
    r = authed.post(f"/episodes/{ep.episode_key}/status", data={"status": "viral"}, htmx=True)
    assert r.status_code == 422


def test_unknown_episode_404(authed, course):
    assert authed.get("/episodes/ep_doesnotexist").status_code == 404
    assert authed.post("/episodes/ep_doesnotexist/status", data={"status": "scripted"}).status_code == 404


def test_publish_asks_for_link_and_length_first(authed, course, db):
    ep = _episode(db, "E012")
    r = authed.post(f"/episodes/{ep.episode_key}/status", data={"status": "published"}, htmx=True)
    assert r.status_code == 200 and 'name="video_url"' in r.text
    assert f'value="{local_today()}"' in r.text  # publish date defaults to today
    db.expire_all()
    assert db.get(EpisodeProgress, ep.episode_key).status == "not_started"

    r = authed.post(f"/episodes/{ep.episode_key}/publish", htmx=True,
                    data={"video_url": "notalink", "length": "abc", "published_on": ""})
    assert r.status_code == 422 and "https://" in r.text

    r = authed.post(f"/episodes/{ep.episode_key}/publish", htmx=True,
                    data={"video_url": "https://youtu.be/abc", "length": "2:05", "published_on": "2026-10-19"})
    assert r.status_code == 200 and r.headers["HX-Trigger"] == "statusChanged"
    db.expire_all()
    p = db.get(EpisodeProgress, ep.episode_key)
    assert (p.status, p.video_url, p.final_length_seconds, str(p.published_on)) == \
        ("published", "https://youtu.be/abc", 125, "2026-10-19")
    assert all(r.episode.code != "E012" for r in services.dashboard(db).up_next)


def test_publish_without_htmx_redirects_to_form(authed, course, db):
    ep = _episode(db, "E012")
    r = authed.post(f"/episodes/{ep.episode_key}/status", data={"status": "published"})
    assert r.status_code == 303 and "publish=1" in r.headers["location"]


def test_production_times_save_and_reload(authed, course, db):
    ep = _episode(db, "E014")
    r = authed.post(f"/episodes/{ep.episode_key}/production", htmx=True,
                    data={"scripting_min": "45", "prep_min": "90", "takes": "3", "editing_min": ""})
    assert r.status_code == 200
    row = db.get(ProductionTime, ep.episode_key)
    assert (row.scripting_min, row.prep_min, row.takes, row.editing_min) == (45, 90, 3, None)
    assert 'value="90"' in authed.get(f"/episodes/{ep.episode_key}").text
    r = authed.post(f"/episodes/{ep.episode_key}/production", htmx=True, data={"scripting_min": "-4"})
    assert r.status_code == 422


def test_module_checklist_commit_and_notes(authed, course, db):
    authed.post("/modules/2/check", data={"field": "learned", "checked": "on"}, htmx=True)
    authed.post("/modules/2/check", data={"field": "built", "checked": "on"}, htmx=True)
    authed.post("/modules/2/check", data={"field": "built"}, htmx=True)  # unticked
    authed.post("/modules/2/notes", data={"commit_sha": "a1b2c3d", "notes": "Tenant from context."}, htmx=True)
    module = services.get_module(db, 2)
    db.expire_all()
    mp = db.get(ModuleProgress, module.module_key)
    assert (mp.learned, mp.built, mp.tested, mp.commit_sha, mp.notes) == \
        (True, False, False, "a1b2c3d", "Tenant from context.")
    page = authed.get("/modules/2").text
    assert "a1b2c3d" in page and "Tenant from context." in page
    assert authed.post("/modules/2/check", data={"field": "hacked"}, htmx=True).status_code == 422


def test_study_sessions_and_weekly_hours(authed, course, db):
    today = local_today()
    r = authed.post("/study", htmx=True, data={"module_number": "3", "minutes": "90", "studied_on": str(today),
                                               "note": "BM25 baseline"})
    assert r.status_code == 200 and r.headers["HX-Trigger"] == "studyLogged"
    last_week = week_start(today) - timedelta(days=1)
    authed.post("/study", htmx=True, data={"module_number": "3", "minutes": "60", "studied_on": str(last_week)})
    assert len(db.scalars(select(StudySession)).all()) == 2
    assert services.dashboard(db).study_minutes_week == 90
    assert "BM25 baseline" in authed.get("/modules/3").text
    assert authed.post("/study", htmx=True, data={"module_number": "3", "minutes": "0"}).status_code == 422
    assert authed.post("/study", htmx=True, data={"module_number": "99", "minutes": "5"}).status_code == 422


def test_filters_and_search(authed, course):
    r = authed.get("/episodes?module=2&type=C")
    assert "E015" in r.text and "E012" not in r.text
    r = authed.get("/episodes?q=unhappy", headers={"HX-Request": "true", "HX-Target": "episode-list"})
    assert "E014" in r.text and "<html" not in r.text


@pytest.mark.parametrize("text,seconds", [("2:05", 125), ("125", 125), ("1:02:05", 3725), (" 0:59 ", 59)])
def test_parse_length(text, seconds):
    assert parse_length(text) == seconds


@pytest.mark.parametrize("text", ["", "abc", "2:75", "0", "1:2:3:4"])
def test_parse_length_rejects(text):
    with pytest.raises(ValueError):
        parse_length(text)


def test_format_length():
    assert format_length(125) == "2:05" and format_length(3725) == "1:02:05" and format_length(None) == ""


def test_digest_for_the_portfolio_admin(authed, course, db):
    ep = _episode(db, "E005")
    authed.post(f"/episodes/{ep.episode_key}/status", data={"status": "edited"}, htmx=True)
    d = authed.get("/api/digest").json()
    assert d["total"] == 87 and d["published"] == 0
    assert {s["status"]: s["count"] for s in d["byStatus"]}["edited"] == 1
    assert [r["key"] for r in d["rings"]] == ["learn", "produce", "publish"]
    assert d["upNext"][0]["code"] == "E005" and d["upNext"][0]["statusLabel"] == "Edited"
    assert {"thisWeek", "target", "perWeek", "remaining", "finishAtPace"} <= d["pace"].keys()


def test_digest_needs_sign_in(client, course):
    assert client.get("/api/digest", follow_redirects=False).headers["location"] == "/login"
