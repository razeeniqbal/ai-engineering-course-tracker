from urllib.parse import quote

from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy.orm import Session

from app import sso
from app.db import get_db
from app.security import LoginLocked, authenticate, csrf_protect, end_session, sso_user, start_session
from app.web import redirect, render

router = APIRouter()


def _here(request: Request, path: str) -> str:
    """Absolute URL of a page on this app, as the browser sees it (Vercel terminates TLS)."""
    proto = request.headers.get("x-forwarded-proto", request.url.scheme)
    return f"{proto}://{request.headers.get('host', request.url.netloc)}{path}"


def sso_url(request: Request, url: str, back: str) -> str | None:
    return f"{url}?next={quote(_here(request, back), safe='')}" if sso.enabled() else None


@router.get("/login")
def login_page(request: Request, db: Session = Depends(get_db)):
    # Only skip the form once the portfolio cookie really opens a session (no account yet → no loop).
    if request.session.get("uid") or sso_user(request, db):
        return redirect("/")
    return render(request, "login.html", sso_login=sso_url(request, sso.LOGIN_URL, "/"))


@router.post("/login", dependencies=[Depends(csrf_protect)])
def login(request: Request, email: str = Form(""), password: str = Form(""), db: Session = Depends(get_db)):
    try:
        user = authenticate(db, email, password)
    except LoginLocked as exc:
        return render(request, "login.html", status_code=429, email=email,
                      sso_login=sso_url(request, sso.LOGIN_URL, "/"),
                      error=f"Too many failed attempts. Try again in {exc.minutes_left} minutes.")
    if user is None:
        return render(request, "login.html", status_code=401, email=email, error="Wrong email or password.",
                      sso_login=sso_url(request, sso.LOGIN_URL, "/"))
    start_session(request, user)
    return redirect("/")


@router.post("/logout", dependencies=[Depends(csrf_protect)])
def logout(request: Request):
    via_sso = request.session.get("sso")
    end_session(request)
    # Signed in through the portfolio: sign out there too, or the cookie would sign straight back in.
    if via_sso and sso.enabled():
        return redirect(sso_url(request, sso.LOGOUT_URL, "/login"))
    return redirect("/login")
