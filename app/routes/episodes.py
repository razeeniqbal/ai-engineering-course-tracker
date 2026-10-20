from datetime import date

from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy.orm import Session

from app import insights, scripts, services
from app.db import get_db
from app.importer import active_version
from app.models import Module
from app.timeutil import local_today, parse_length, to_local, utcnow
from app.web import back_path, is_htmx, optional_int, redirect, render

router = APIRouter()


@router.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):
    return render(request, "dashboard.html", d=services.dashboard(db), today=local_today(), page="dashboard")


@router.get("/dashboard/summary")
def dashboard_summary(request: Request, db: Session = Depends(get_db)):
    return render(request, "partials/dashboard_summary.html", d=services.dashboard(db))


@router.get("/api/digest")
def digest(db: Session = Depends(get_db)):
    """At-a-glance numbers for the portfolio admin hub (signed-in only, like every page here)."""
    d = services.dashboard(db)
    counts = {slug: n for slug, _, n in d.by_status}
    return {
        "total": d.total,
        "published": counts.get("published", 0),
        "byStatus": [{"status": slug, "label": label, "count": n} for slug, label, n in d.by_status],
        "rings": [{"key": r.key, "label": r.label, "percent": r.percent, "detail": r.detail} for r in d.rings],
        "studyMinutesWeek": d.study_minutes_week,
        "streak": d.streak,
        "pace": {
            "thisWeek": d.pace.this_week,
            "target": d.pace.target,
            "perWeek": d.pace.per_week,
            "remaining": d.pace.remaining,
            "finishAtPace": d.pace.finish_at_pace.isoformat() if d.pace.finish_at_pace else None,
        },
        "upNext": [
            {"key": r.episode.episode_key, "code": r.episode.code, "title": r.episode.title,
             "status": r.progress.status, "statusLabel": r.status_label}
            for r in d.up_next[:3]
        ],
    }


@router.get("/episodes")
def episodes(request: Request, module: str = "", status: str = "", type: str = "", q: str = "",
             db: Session = Depends(get_db)):
    module_number = int(module) if module.isdigit() else None
    rows = services.episode_rows(db, module_number, status or None, type or None, q or None)
    version = active_version(db)
    modules = (db.query(Module).filter(Module.version_id == version.id).order_by(Module.number).all()
               if version else [])
    context = dict(rows=rows, modules=modules, f={"module": module, "status": status, "type": type, "q": q},
                   page="episodes")
    if is_htmx(request) and request.headers.get("hx-target") == "episode-list":
        return render(request, "partials/episode_list.html", **context)
    return render(request, "episodes.html", **context)


def _detail_context(db: Session, row: services.EpisodeRow) -> dict:
    key = row.episode.episode_key
    times = services.production_time(db, key)
    nav = insights.neighbours(db, row.episode)
    return dict(row=row, history=services.status_history(db, key), times=times,
                total_minutes=insights.production_minutes(times), nav=nav,
                stage=insights.STAGE[row.progress.status], today=local_today(), page="episodes",
                script_stats=scripts.stats(row.progress.script_markdown, row.episode.type),
                script_outline=scripts.outline(row.episode, nav.next))


@router.get("/episodes/{episode_key}")
def episode_detail(request: Request, episode_key: str, db: Session = Depends(get_db)):
    return render(request, "episode_detail.html", **_detail_context(db, services.get_episode(db, episode_key)))


@router.get("/episodes/{episode_key}/status")
def status_control(request: Request, episode_key: str, db: Session = Depends(get_db)):
    return render(request, "partials/status_control.html", row=services.get_episode(db, episode_key))


@router.post("/episodes/{episode_key}/status")
def set_status(request: Request, episode_key: str, status: str = Form(...), db: Session = Depends(get_db)):
    row = services.get_episode(db, episode_key)
    if status == "published" and services.needs_publish_details(row.progress):
        # Ask for the link and length before marking it published.
        if is_htmx(request):
            return render(request, "partials/publish_form.html", row=row, today=local_today())
        return redirect(f"/episodes/{episode_key}?publish=1#publish")
    try:
        services.change_status(db, episode_key, status)
    except ValueError as exc:
        return render(request, "partials/status_control.html", status_code=422, row=row, error=str(exc))
    if not is_htmx(request):
        return redirect(back_path(request, f"/episodes/{episode_key}"))
    response = render(request, "partials/status_control.html", row=services.get_episode(db, episode_key))
    response.headers["HX-Trigger"] = "statusChanged"
    return response


@router.post("/episodes/{episode_key}/publish")
def publish(request: Request, episode_key: str, video_url: str = Form(""), length: str = Form(""),
            published_on: str = Form(""), db: Session = Depends(get_db)):
    row = services.get_episode(db, episode_key)
    errors = []
    video_url = video_url.strip()
    if not video_url.startswith(("https://", "http://")) or len(video_url) > 500:
        errors.append("Enter the full video link, starting with https://")
    try:
        seconds = parse_length(length)
    except ValueError as exc:
        errors.append(f"Length: {exc}")
    try:
        day = date.fromisoformat(published_on) if published_on else local_today()
    except ValueError:
        errors.append("Publish date must be a valid date")
    if errors:
        values = {"video_url": video_url, "length": length, "published_on": published_on}
        if is_htmx(request):
            return render(request, "partials/publish_form.html", status_code=422, row=row, today=local_today(),
                          errors=errors, values=values)
        return render(request, "episode_detail.html", status_code=422, errors=errors, values=values,
                      **_detail_context(db, row))
    services.publish(db, episode_key, video_url, seconds, day)
    if not is_htmx(request):
        return redirect(f"/episodes/{episode_key}")
    response = render(request, "partials/status_control.html", row=services.get_episode(db, episode_key))
    response.headers["HX-Trigger"] = "statusChanged"
    return response


@router.post("/episodes/{episode_key}/production")
def save_production(request: Request, episode_key: str, scripting_min: str = Form(""), prep_min: str = Form(""),
                    takes: str = Form(""), editing_min: str = Form(""), db: Session = Depends(get_db)):
    services.get_episode(db, episode_key)
    try:
        values = dict(scripting_min=optional_int(scripting_min, "Scripting minutes"),
                      prep_min=optional_int(prep_min, "Demo prep minutes"),
                      takes=optional_int(takes, "Recording takes", 1000),
                      editing_min=optional_int(editing_min, "Editing minutes"))
    except ValueError as exc:
        return render(request, "partials/saved.html", status_code=422, error=str(exc))
    services.save_production_time(db, episode_key, **values)
    if not is_htmx(request):
        return redirect(f"/episodes/{episode_key}")
    return render(request, "partials/saved.html")


@router.post("/episodes/{episode_key}/script")
def save_script(request: Request, episode_key: str, script_markdown: str = Form(""),
                db: Session = Depends(get_db)):
    row = services.get_episode(db, episode_key)
    if len(script_markdown) > scripts.MAX_SCRIPT_CHARS:
        return render(request, "partials/script_status.html", status_code=422,
                      error=f"Script is longer than {scripts.MAX_SCRIPT_CHARS:,} characters; not saved.")
    services.save_script(db, episode_key, script_markdown)
    if not is_htmx(request):
        return redirect(f"/episodes/{episode_key}#script")
    return render(request, "partials/script_status.html", saved_at=to_local(utcnow()),
                  s=scripts.stats(script_markdown, row.episode.type))
