from datetime import date

from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy.orm import Session

from app import services
from app.db import get_db
from app.models import StudySession
from app.timeutil import local_today
from app.web import back_path, is_htmx, redirect, render

router = APIRouter()

CHECK_FIELDS = ("learned", "built", "tested")


@router.get("/modules")
def modules(request: Request, db: Session = Depends(get_db)):
    return render(request, "modules.html", rows=services.module_rows(db), page="modules")


@router.get("/modules/{number}")
def module_detail(request: Request, number: int, db: Session = Depends(get_db)):
    module = services.get_module(db, number)
    return render(request, "module_detail.html", module=module,
                  progress=services.module_progress(db, module.module_key),
                  rows=services.episode_rows(db, module_number=number),
                  sessions=services.study_sessions(db, module.module_key), today=local_today(), page="modules")


@router.post("/modules/{number}/check")
def toggle_check(request: Request, number: int, field: str = Form(...), checked: str = Form(""),
                 db: Session = Depends(get_db)):
    if field not in CHECK_FIELDS:
        return render(request, "partials/saved.html", status_code=422, error="Unknown checkbox")
    module = services.get_module(db, number)
    progress = services.module_progress(db, module.module_key)
    setattr(progress, field, checked == "on")
    db.commit()
    if not is_htmx(request):
        return redirect(f"/modules/{number}")
    return render(request, "partials/saved.html")


@router.post("/modules/{number}/notes")
def save_notes(request: Request, number: int, commit_sha: str = Form(""), notes: str = Form(""),
               db: Session = Depends(get_db)):
    module = services.get_module(db, number)
    progress = services.module_progress(db, module.module_key)
    progress.commit_sha = commit_sha.strip()[:64] or None
    progress.notes = notes.strip() or None
    db.commit()
    if not is_htmx(request):
        return redirect(f"/modules/{number}")
    return render(request, "partials/saved.html")


@router.post("/study")
def log_study(request: Request, module_number: str = Form(""), minutes: str = Form(""), studied_on: str = Form(""),
              note: str = Form(""), db: Session = Depends(get_db)):
    try:
        if not module_number.isdigit():
            raise ValueError("Choose a module")
        module = services.get_module(db, int(module_number))
        if not minutes.strip().isdigit():
            raise ValueError("Minutes must be a whole number")
        day = date.fromisoformat(studied_on) if studied_on else local_today()
        services.add_study_session(db, module.module_key, day, int(minutes), note)
    except (ValueError, services.NotFound) as exc:
        message = "Choose a module" if isinstance(exc, services.NotFound) else str(exc)
        if is_htmx(request):
            return render(request, "partials/saved.html", status_code=422, error=message)
        return render(request, "error.html", status_code=422, message=message)
    if is_htmx(request):
        response = render(request, "partials/saved.html", message=f"Logged {int(minutes)} min")
        response.headers["HX-Trigger"] = "studyLogged"
        return response
    return redirect(back_path(request, "/"))


@router.post("/study/{session_id}/delete")
def delete_study(request: Request, session_id: int, db: Session = Depends(get_db)):
    row = db.get(StudySession, session_id)
    if row is not None:
        db.delete(row)
        db.commit()
    return redirect(back_path(request, "/modules"))
