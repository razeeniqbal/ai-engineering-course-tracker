import csv
import io
import json
import zipfile

from sqlalchemy import select

from app.export import TABLE_NAMES
from app.models import Episode


def test_json_export_has_every_table_and_no_credentials(authed, course, db):
    ep = db.scalar(select(Episode).where(Episode.code == "E001"))
    authed.post(f"/episodes/{ep.episode_key}/status", data={"status": "scripted"}, htmx=True)
    r = authed.get("/export/json")
    assert r.status_code == 200
    assert "attachment" in r.headers["content-disposition"]
    data = json.loads(r.text)
    assert set(data["tables"]) == set(TABLE_NAMES)
    assert len(data["tables"]["episodes"]) == 87
    assert len(data["tables"]["status_events"]) == 1
    user = data["tables"]["users"][0]
    assert "password_hash" not in user and "totp_secret" not in user
    assert "argon2" not in r.text


def test_csv_zip_has_one_file_per_table(authed, course):
    r = authed.get("/export/csv")
    assert r.status_code == 200
    with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
        assert sorted(zf.namelist()) == sorted(f"{t}.csv" for t in TABLE_NAMES)
        rows = list(csv.DictReader(io.StringIO(zf.read("modules.csv").decode("utf-8-sig"))))
    assert len(rows) == 16
    assert json.loads(rows[1]["lab_steps"])[0].startswith("Write 100 descriptions")


def test_single_table_csv(authed, course):
    r = authed.get("/export/csv/episodes")
    rows = list(csv.DictReader(io.StringIO(r.content.decode("utf-8-sig"))))
    assert len(rows) == 87 and rows[0]["code"] == "E001"
    assert authed.get("/export/csv/secrets").status_code == 404
