"""Template setup and small helpers shared by the route modules."""

from pathlib import Path
from urllib.parse import urlsplit

from fastapi import Request
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from app.models import STATUS_LABELS, STATUSES
from app.security import csrf_token
from app.timeutil import format_length, to_local

templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
templates.env.globals.update(STATUSES=STATUSES, STATUS_LABELS=STATUS_LABELS)
templates.env.filters["local"] = lambda dt, fmt="%d %b %Y, %H:%M": (to_local(dt).strftime(fmt) if dt else "")
templates.env.filters["duration"] = format_length
templates.env.filters["hours"] = lambda minutes: f"{(minutes or 0) / 60:.1f}"


def render(request: Request, name: str, status_code: int = 200, **context) -> Response:
    context.setdefault("csrf_token", csrf_token(request))
    return templates.TemplateResponse(request, name, context, status_code=status_code)


def is_htmx(request: Request) -> bool:
    return request.headers.get("hx-request") == "true"


def redirect(url: str) -> RedirectResponse:
    return RedirectResponse(url, status_code=303)


def back_path(request: Request, default: str) -> str:
    """The page the form came from, as a local path only (never an outside URL)."""
    path = urlsplit(request.headers.get("referer", "")).path
    return path if path.startswith("/") and not path.startswith("//") else default


def optional_int(value: str | None, name: str, maximum: int = 100_000) -> int | None:
    value = (value or "").strip()
    if not value:
        return None
    if not value.isdigit() or int(value) > maximum:
        raise ValueError(f"{name} must be a whole number from 0 to {maximum}")
    return int(value)
