from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db import get_db
from app.export import TABLE_NAMES, export_csv_zip, export_json, table_csv
from app.importer import CourseImportError, active_version, import_course
from app.models import User
from app.security import check_new_password, current_user, hash_password, start_session, verify_password
from app.timeutil import local_today
from app.web import redirect, render

router = APIRouter()

MAX_UPLOAD_BYTES = 2 * 1024 * 1024


def _settings_page(request: Request, db: Session, status_code: int = 200, **extra):
    return render(request, "settings.html", status_code=status_code, version=active_version(db),
                  tables=TABLE_NAMES, page="settings", **extra)


@router.get("/settings")
def settings_page(request: Request, db: Session = Depends(get_db)):
    return _settings_page(request, db, notice=request.query_params.get("notice"))


@router.post("/settings/import")
async def upload_course(request: Request, course_file: UploadFile = File(...), label: str = Form(""),
                        db: Session = Depends(get_db)):
    raw = await course_file.read(MAX_UPLOAD_BYTES + 1)
    if len(raw) > MAX_UPLOAD_BYTES:
        return _settings_page(request, db, 413, import_errors=["File is larger than 2 MB."])
    try:
        markdown = raw.decode("utf-8-sig")
        version = import_course(db, markdown, label or None)
    except UnicodeDecodeError:
        return _settings_page(request, db, 422, import_errors=["File must be UTF-8 markdown."])
    except CourseImportError as exc:
        db.rollback()
        return _settings_page(request, db, 422, import_errors=exc.errors)
    return redirect(f"/settings?notice=Imported+course+{version.label}")


@router.post("/settings/password")
def change_password(request: Request, current_password: str = Form(""), new_password: str = Form(""),
                    confirm_password: str = Form(""), user: User = Depends(current_user),
                    db: Session = Depends(get_db)):
    error = None
    if not verify_password(user.password_hash, current_password):
        error = "Current password is wrong."
    elif new_password != confirm_password:
        error = "New passwords don't match."
    else:
        try:
            check_new_password(new_password)
        except ValueError as exc:
            error = str(exc)
    if error:
        return _settings_page(request, db, 422, password_error=error)
    user.password_hash = hash_password(new_password)
    user.session_version += 1  # signs out every other device
    db.commit()
    start_session(request, user)
    return redirect("/settings?notice=Password+changed")


def _download(content: str | bytes, filename: str, media_type: str) -> Response:
    return Response(content, media_type=media_type,
                    headers={"Content-Disposition": f'attachment; filename="{filename}"'})


@router.get("/export/json")
def download_json(db: Session = Depends(get_db)):
    return _download(export_json(db), f"course-tracker-{local_today()}.json", "application/json")


@router.get("/export/csv")
def download_csv_zip(db: Session = Depends(get_db)):
    return _download(export_csv_zip(db), f"course-tracker-csv-{local_today()}.zip", "application/zip")


@router.get("/export/csv/{table}")
def download_table_csv(table: str, db: Session = Depends(get_db)):
    if table not in TABLE_NAMES:
        return Response("Unknown table", status_code=404)
    return _download("﻿" + table_csv(db, table), f"{table}-{local_today()}.csv", "text/csv; charset=utf-8")
