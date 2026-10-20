import json

from sqlalchemy import select

from app import scripts
from app.models import Episode, EpisodeProgress

PILOT_STYLE = """**0:00–0:15 · Hook**
*Screen: chat answer "Your March revenue was 10,249 MYR."*
> I asked an AI for my company's March revenue.

**1:50–2:00 · Takeaway**
*Screen: "If it must be exact, compute it."*
> If it must be exact, compute it.
"""


def test_counts_only_spoken_lines_when_present():
    s = scripts.stats(PILOT_STYLE, "B")
    assert s.spoken_only and s.words == 9 + 7  # screen directions and headings are not spoken
    assert (s.low, s.high) == (180, 240)


def test_counts_everything_without_blockquotes_and_judges_length():
    assert scripts.stats("one two three", "C").words == 3
    assert scripts.stats(None, "C").verdict == "empty"
    assert scripts.stats("word " * 100, "C").verdict == "short"
    assert scripts.stats("word " * 240, "C").verdict == "on-target"
    long = scripts.stats("word " * 300, "C")
    assert long.verdict == "over" and long.duration == "2:18"


def test_outline_uses_the_spec(db, course):
    e012 = db.scalar(select(Episode).where(Episode.code == "E012"))
    e013 = db.scalar(select(Episode).where(Episode.code == "E013"))
    text = scripts.outline(e012, e013)
    assert text.startswith("**0:00–0:15 · Hook**")
    assert f"> {e012.hook}" in text and f"> {e012.claim}" in text
    assert f"*Screen: {e012.show}*" in text
    assert "Next: An API with a contract." in text
    assert scripts.stats(text, "B").spoken_only


def test_autosave_saves_and_reloads(authed, course, db):
    ep = db.scalar(select(Episode).where(Episode.code == "E001"))
    r = authed.post(f"/episodes/{ep.episode_key}/script", htmx=True,
                    data={"script_markdown": "> Hello there\r\n> second line\r\n"})
    assert r.status_code == 200 and "Saved" in r.text
    db.expire_all()
    assert db.get(EpisodeProgress, ep.episode_key).script_markdown == "> Hello there\n> second line"
    page = authed.get(f"/episodes/{ep.episode_key}").text
    assert "&gt; Hello there" in page and "4 spoken words" in page
    assert "Insert two-minute outline" in page


def test_empty_script_clears_it_and_too_long_is_refused(authed, course, db):
    ep = db.scalar(select(Episode).where(Episode.code == "E001"))
    authed.post(f"/episodes/{ep.episode_key}/script", htmx=True, data={"script_markdown": "> draft"})
    authed.post(f"/episodes/{ep.episode_key}/script", htmx=True, data={"script_markdown": ""})
    db.expire_all()
    assert db.get(EpisodeProgress, ep.episode_key).script_markdown is None
    r = authed.post(f"/episodes/{ep.episode_key}/script", htmx=True,
                    data={"script_markdown": "x" * (scripts.MAX_SCRIPT_CHARS + 1)})
    assert r.status_code == 422


def test_script_save_needs_csrf_and_sign_in(client, owner, course, db):
    ep = db.scalar(select(Episode).where(Episode.code == "E001"))
    r = client.post(f"/episodes/{ep.episode_key}/script", data={"script_markdown": "x"}, follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == "/login"


def test_scripts_are_in_the_export(authed, course, db):
    ep = db.scalar(select(Episode).where(Episode.code == "E002"))
    authed.post(f"/episodes/{ep.episode_key}/script", htmx=True, data={"script_markdown": "> exported"})
    rows = json.loads(authed.get("/export/json").text)["tables"]["episode_progress"]
    assert any(r["script_markdown"] == "> exported" for r in rows)
