"""Export every table as JSON (one file) or CSV (one file per table, zipped)."""

import csv
import io
import json
import zipfile
from datetime import date, datetime

from sqlalchemy import inspect, select
from sqlalchemy.orm import Session

from app.models import EXPORT_TABLES, User
from app.timeutil import as_utc, utcnow

# Credentials never leave the database through an export.
EXCLUDED_COLUMNS = {User.__tablename__: {"password_hash", "totp_secret"}}
TABLE_NAMES = [m.__tablename__ for m in EXPORT_TABLES]


def _value(v: object) -> object:
    if isinstance(v, datetime):
        return as_utc(v).isoformat()
    if isinstance(v, date):
        return v.isoformat()
    return v


def _columns(model) -> list[str]:
    skip = EXCLUDED_COLUMNS.get(model.__tablename__, set())
    return [c.key for c in inspect(model).columns if c.key not in skip]


def table_rows(db: Session, model) -> tuple[list[str], list[dict]]:
    cols = _columns(model)
    pk = inspect(model).primary_key
    rows = db.scalars(select(model).order_by(*pk)).all()
    return cols, [{c: _value(getattr(r, c)) for c in cols} for r in rows]


def export_json(db: Session) -> str:
    tables = {m.__tablename__: table_rows(db, m)[1] for m in EXPORT_TABLES}
    return json.dumps({"exported_at": utcnow().isoformat(), "tables": tables}, ensure_ascii=False, indent=2)


def table_csv(db: Session, name: str) -> str:
    model = next(m for m in EXPORT_TABLES if m.__tablename__ == name)
    cols, rows = table_rows(db, model)
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=cols)
    writer.writeheader()
    for row in rows:
        writer.writerow({k: json.dumps(v) if isinstance(v, (list, dict)) else v for k, v in row.items()})
    return buf.getvalue()


def export_csv_zip(db: Session) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in TABLE_NAMES:
            # BOM so Excel opens the UTF-8 file correctly.
            zf.writestr(f"{name}.csv", "﻿" + table_csv(db, name))
    return buf.getvalue()
