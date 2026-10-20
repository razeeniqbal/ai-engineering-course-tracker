from datetime import date, timedelta

from sqlalchemy import select

from app import insights, services
from app.models import Episode, ModuleProgress
from app.timeutil import local_today, week_start

MON = date(2026, 10, 19)  # a Monday


def test_pace_with_no_publishing_uses_target_only():
    p = insights.pace([], remaining=87, today=MON)
    assert (p.this_week, p.per_week, p.finish_at_pace) == (0, 0.0, None)
    assert p.finish_at_target == MON + timedelta(weeks=29)  # ceil(87 / 3)


def test_pace_counts_this_week_and_projects_finish():
    today = MON + timedelta(days=3)  # Thursday
    published = [MON, MON + timedelta(days=1), MON - timedelta(days=2), MON - timedelta(days=9),
                 MON - timedelta(days=16), MON - timedelta(days=23),
                 MON - timedelta(days=40)]  # 6 in the last 4 weeks, 1 older
    p = insights.pace(published, remaining=81, today=today)
    assert p.this_week == 2
    assert p.per_week == 1.5
    assert p.finish_at_pace == today + timedelta(weeks=54)  # ceil(81 / 1.5)


def test_pace_early_on_uses_time_since_first_publish():
    today = MON + timedelta(days=6)
    p = insights.pace([MON, MON + timedelta(days=2)], remaining=10, today=today)
    assert p.per_week == 2.0  # two in the first week, not two spread over four weeks


def test_pace_when_everything_is_published():
    assert insights.pace([MON], remaining=0, today=MON).finish_at_pace == MON


def test_streak_counts_back_from_today_or_yesterday():
    days = {MON, MON - timedelta(days=1), MON - timedelta(days=2), MON - timedelta(days=5)}
    assert insights.streak(days, today=MON) == 3
    assert insights.streak(days, today=MON + timedelta(days=1)) == 3  # today still empty: streak alive
    assert insights.streak(days, today=MON + timedelta(days=2)) == 0
    assert insights.streak(set(), today=MON) == 0


def test_rings():
    statuses = ["published", "not_started", "scripted", "edited"]
    checks = [ModuleProgress(learned=True, built=True, tested=False), ModuleProgress(learned=True, built=False,
                                                                                   tested=False)]
    learn, produce, publish = insights.rings(statuses, checks, module_count=2)
    assert (learn.percent, publish.percent) == (50, 25)
    assert produce.percent == round(100 * (4 + 0 + 1 + 3) / 16)


def test_weekly_chart_buckets_by_monday(authed, course, db):
    today = local_today()
    this_week = week_start(today)
    authed.post("/study", htmx=True, data={"module_number": "0", "minutes": "90", "studied_on": str(today)})
    authed.post("/study", htmx=True, data={"module_number": "0", "minutes": "30",
                                           "studied_on": str(this_week - timedelta(days=1))})
    authed.post("/study", htmx=True, data={"module_number": "0", "minutes": "45",
                                           "studied_on": str(this_week - timedelta(weeks=12))})  # outside window
    chart = insights.weekly_study_chart(db, today=today)
    assert len(chart.bars) == 8
    assert chart.bars[-1].week == this_week and chart.bars[-1].minutes == 90
    assert chart.bars[-2].minutes == 30
    assert chart.total_minutes == 120
    assert chart.max_hours == 2
    tallest = max(chart.bars, key=lambda b: b.height)
    assert tallest is chart.bars[-1] and tallest.height > 0


def test_activity_feed_merges_status_and_study(authed, course, db):
    ep = db.scalar(select(Episode).where(Episode.code == "E003"))
    authed.post(f"/episodes/{ep.episode_key}/status", data={"status": "scripted"}, htmx=True)
    authed.post("/study", htmx=True, data={"module_number": "1", "minutes": "25", "note": "baselines"})
    feed = insights.activity(db)
    kinds = {a.kind for a in feed}
    assert kinds == {"status", "study"}
    status_item = next(a for a in feed if a.kind == "status")
    assert "E003" in status_item.title and status_item.detail == "Not started → Scripted"
    assert insights.streak(insights.active_days(db)) == 1


def test_neighbours_and_module_stats(authed, course, db):
    e012 = db.scalar(select(Episode).where(Episode.code == "E012"))
    nav = insights.neighbours(db, e012)
    assert (nav.prev.code, nav.next.code) == ("E011", "E013")
    first = db.scalar(select(Episode).where(Episode.code == "E001"))
    assert insights.neighbours(db, first).prev is None

    authed.post(f"/episodes/{e012.episode_key}/production", htmx=True,
                data={"scripting_min": "30", "prep_min": "20", "takes": "4", "editing_min": "40"})
    authed.post("/study", htmx=True, data={"module_number": "2", "minutes": "50"})
    module = services.get_module(db, 2)
    stats = insights.module_stats(db, module)
    assert (stats.total, stats.published, stats.production_minutes, stats.study_minutes) == (7, 0, 90, 50)
    assert dict((s, n) for s, _, n in stats.breakdown)["not_started"] == 7


def test_pages_show_the_new_details(authed, course, db):
    page = authed.get("/").text
    for text in ("Progress", "Study hours per week", "Recent activity", "Streak", "Finish", "Episodes by status"):
        assert text in page, text
    e012 = db.scalar(select(Episode).where(Episode.code == "E012"))
    detail = authed.get(f"/episodes/{e012.episode_key}").text
    assert "E011" in detail and "E013" in detail and 'aria-current="step"' in detail
    module = authed.get("/modules/2").text
    assert "Checklist" in module and "Production" in module and 'role="switch"' in module
