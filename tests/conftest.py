import os
import re
import tempfile
from pathlib import Path

# Settings are read at import time, so configure the environment before importing the app.
os.environ["APP_ENV"] = "test"
os.environ.setdefault("SECRET_KEY", "test-secret")
_tmp_db = Path(tempfile.gettempdir()) / f"course_tracker_test_{os.getpid()}.db"
os.environ["DATABASE_URL"] = os.getenv("TEST_DATABASE_URL") or f"sqlite:///{_tmp_db.as_posix()}"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.db import Base, SessionLocal, engine  # noqa: E402
from app.importer import import_course  # noqa: E402
from app.main import app  # noqa: E402
from app.models import User  # noqa: E402
from app.security import hash_password  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
COURSE_PATH = ROOT / "course" / "AI_Engineering_Course_Razeen_v7.md"
EMAIL = "owner@example.com"
PASSWORD = "correct horse battery staple"
CSRF_RE = re.compile(r'name="csrf_token" value="([^"]+)"')


@pytest.fixture(autouse=True)
def fresh_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db():
    with SessionLocal() as session:
        yield session


@pytest.fixture
def course_md() -> str:
    return COURSE_PATH.read_text(encoding="utf-8")


@pytest.fixture
def owner(db):
    user = User(email=EMAIL, password_hash=hash_password(PASSWORD))
    db.add(user)
    db.commit()
    return user


@pytest.fixture
def course(db, course_md):
    return import_course(db, course_md)


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def csrf_from(html: str) -> str:
    match = CSRF_RE.search(html)
    assert match, "no CSRF token on page"
    return match.group(1)


def login(client: TestClient, email: str = EMAIL, password: str = PASSWORD):
    token = csrf_from(client.get("/login").text)
    return client.post("/login", data={"email": email, "password": password, "csrf_token": token},
                       follow_redirects=False)


class AuthedClient:
    """TestClient wrapper that sends the CSRF header on every POST, like the HTMX pages do."""

    def __init__(self, client: TestClient):
        self.client = client
        self.token = csrf_from(client.get("/settings").text)

    def get(self, url, **kw):
        return self.client.get(url, **kw)

    def post(self, url, htmx=False, **kw):
        headers = {"X-CSRF-Token": self.token, **kw.pop("headers", {})}
        if htmx:
            headers["HX-Request"] = "true"
        kw.setdefault("follow_redirects", False)
        return self.client.post(url, headers=headers, **kw)


@pytest.fixture
def authed(client, owner):
    assert login(client).status_code == 303
    return AuthedClient(client)
