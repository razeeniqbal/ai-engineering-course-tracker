from datetime import timedelta

from sqlalchemy import select

from app.models import User
from app.timeutil import as_utc, utcnow
from tests.conftest import EMAIL, PASSWORD, csrf_from, login


def test_password_stored_as_argon2(owner):
    assert owner.password_hash.startswith("$argon2id$")
    assert PASSWORD not in owner.password_hash


def test_pages_require_sign_in(client):
    for url in ("/", "/episodes", "/modules", "/settings", "/export/json"):
        r = client.get(url, follow_redirects=False)
        assert r.status_code == 303 and r.headers["location"] == "/login", url


def test_htmx_request_without_session_gets_hx_redirect(client):
    r = client.get("/dashboard/summary", headers={"HX-Request": "true"})
    assert r.status_code == 401 and r.headers["HX-Redirect"] == "/login"


def test_sign_in_and_out(client, owner):
    r = login(client)
    assert r.status_code == 303 and r.headers["location"] == "/"
    assert client.get("/", follow_redirects=False).status_code == 200
    token = csrf_from(client.get("/").text)
    client.post("/logout", data={"csrf_token": token})
    assert client.get("/", follow_redirects=False).status_code == 303


def test_session_cookie_flags(client, owner):
    r = login(client)
    cookie = r.headers["set-cookie"].lower()
    assert "httponly" in cookie and "samesite=lax" in cookie


def test_wrong_password_and_unknown_email(client, owner):
    assert login(client, password="wrong password!").status_code == 401
    assert login(client, email="nobody@example.com").status_code == 401


def test_ten_failures_lock_for_15_minutes(client, owner, db):
    for _ in range(9):
        assert login(client, password="nope nope nope").status_code == 401
    r = login(client, password="nope nope nope")
    assert r.status_code == 429 and "Too many failed attempts" in r.text
    # Even the right password is refused while locked.
    assert login(client).status_code == 429

    user = db.scalar(select(User).where(User.email == EMAIL))
    db.refresh(user)
    remaining = as_utc(user.locked_until) - utcnow()
    assert timedelta(minutes=14) < remaining <= timedelta(minutes=15)

    # Once the lock expires the right password works and the counter resets.
    user.locked_until = utcnow() - timedelta(seconds=1)
    db.commit()
    assert login(client).status_code == 303
    db.refresh(user)
    assert user.failed_login_count == 0 and user.locked_until is None


def test_success_resets_failure_count(client, owner, db):
    for _ in range(5):
        login(client, password="nope nope nope")
    assert login(client).status_code == 303
    db.refresh(owner)
    assert owner.failed_login_count == 0


def test_post_without_csrf_token_is_rejected(client, owner):
    login(client)
    r = client.post("/study", data={"module_number": "0", "minutes": "30"})
    assert r.status_code == 403
    r = client.post("/study", data={"module_number": "0", "minutes": "30"}, headers={"X-CSRF-Token": "forged"})
    assert r.status_code == 403


def test_login_form_requires_csrf(client, owner):
    client.get("/login")
    r = client.post("/login", data={"email": EMAIL, "password": PASSWORD})
    assert r.status_code == 403


def test_password_change_signs_out_other_sessions(authed, client, owner):
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as other:
        assert login(other).status_code == 303
        r = authed.post("/settings/password", data={"current_password": PASSWORD, "new_password": "a brand new password",
                                                    "confirm_password": "a brand new password"})
        assert r.status_code == 303
        assert other.get("/", follow_redirects=False).status_code == 303  # old session dead
    assert authed.get("/", follow_redirects=False).status_code == 200  # this one re-issued
    assert login(client, password="a brand new password").status_code == 303


def test_password_change_validates(authed):
    r = authed.post("/settings/password", data={"current_password": "wrong", "new_password": "x" * 12,
                                                "confirm_password": "x" * 12})
    assert r.status_code == 422 and "Current password is wrong" in r.text
    r = authed.post("/settings/password", data={"current_password": PASSWORD, "new_password": "short",
                                                "confirm_password": "short"})
    assert r.status_code == 422 and "at least 12" in r.text


def test_security_headers(client):
    r = client.get("/login")
    assert "default-src 'self'" in r.headers["content-security-policy"]
    assert r.headers["x-frame-options"] == "DENY"
