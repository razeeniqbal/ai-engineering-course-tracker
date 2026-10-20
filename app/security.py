"""Single-user sign-in: Argon2 hashes, account lockout, session checks and CSRF.

The portfolio admin's sign-in cookie (app/sso.py) also opens a session, for the one
user this app has; such a session ends as soon as that cookie is gone or expired.
"""

import hmac
import secrets
from datetime import timedelta

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError
from fastapi import Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import sso
from app.config import settings
from app.db import get_db
from app.models import User
from app.timeutil import as_utc, utcnow

hasher = PasswordHasher()
# Verified against when the email is unknown, so timing doesn't reveal which emails exist.
_DUMMY_HASH = hasher.hash("not-a-real-password")

MIN_PASSWORD_LENGTH = 12


def hash_password(password: str) -> str:
    return hasher.hash(password)


def check_new_password(password: str) -> None:
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValueError(f"Password must be at least {MIN_PASSWORD_LENGTH} characters")


def verify_password(password_hash: str, password: str) -> bool:
    try:
        return hasher.verify(password_hash, password)
    except (VerificationError, InvalidHashError):
        return False


class LoginLocked(Exception):
    def __init__(self, minutes_left: int):
        self.minutes_left = minutes_left


def authenticate(db: Session, email: str, password: str) -> User | None:
    """Return the user on success, None on bad credentials; raise LoginLocked while locked.

    Every failure counts against the account with that email. The tenth failure locks it
    for 15 minutes, and while locked even the right password is refused.
    """
    user = db.scalar(select(User).where(User.email == email.strip().lower()))
    if user is None:
        verify_password(_DUMMY_HASH, password)
        return None

    now = utcnow()
    if user.locked_until is not None:
        locked_until = as_utc(user.locked_until)
        if locked_until > now:
            raise LoginLocked(max(1, int((locked_until - now).total_seconds() // 60) + 1))
        user.locked_until = None
        user.failed_login_count = 0

    if not verify_password(user.password_hash, password):
        user.failed_login_count += 1
        if user.failed_login_count >= settings.lockout_threshold:
            user.locked_until = now + timedelta(minutes=settings.lockout_minutes)
            db.commit()
            raise LoginLocked(settings.lockout_minutes)
        db.commit()
        return None

    user.failed_login_count = 0
    if hasher.check_needs_rehash(user.password_hash):
        user.password_hash = hash_password(password)
    db.commit()
    return user


# --- sessions ---------------------------------------------------------------

def start_session(request: Request, user: User) -> None:
    request.session.clear()
    request.session.update({"uid": user.id, "sv": user.session_version, "csrf": secrets.token_urlsafe(32)})


def end_session(request: Request) -> None:
    request.session.clear()


class NotAuthenticated(Exception):
    pass


def sso_signed_in(request: Request) -> bool:
    return sso.verify(request.cookies.get(sso.COOKIE)) is not None


def sso_user(request: Request, db: Session) -> User | None:
    """Open a session from the portfolio cookie. The app is single-user: it is the first account."""
    if not sso_signed_in(request):
        return None
    user = db.scalar(select(User).order_by(User.id).limit(1))
    if user is not None:
        start_session(request, user)
        request.session["sso"] = True
    return user


def current_user(request: Request, db: Session = Depends(get_db)) -> User:
    if request.session.get("sso") and not sso_signed_in(request):
        request.session.clear()  # signed out of (or expired at) the portfolio
    uid = request.session.get("uid")
    user = db.get(User, uid) if uid is not None else None
    if user is None or request.session.get("sv") != user.session_version:
        request.session.clear()
        user = sso_user(request, db)
        if user is None:
            raise NotAuthenticated()
    return user


# --- CSRF -------------------------------------------------------------------

def csrf_token(request: Request) -> str:
    token = request.session.get("csrf")
    if not token:
        token = secrets.token_urlsafe(32)
        request.session["csrf"] = token
    return token


async def csrf_protect(request: Request) -> None:
    """Check the token on every state-changing request (form field or HTMX header)."""
    if request.method in {"GET", "HEAD", "OPTIONS"}:
        return
    expected = request.session.get("csrf")
    sent = request.headers.get("x-csrf-token")
    if not sent:
        content_type = request.headers.get("content-type", "")
        if content_type.startswith(("application/x-www-form-urlencoded", "multipart/form-data")):
            sent = (await request.form()).get("csrf_token")
    if not expected or not sent or not hmac.compare_digest(str(sent), expected):
        raise HTTPException(status_code=403, detail="Invalid or missing CSRF token. Reload the page and try again.")
