"""Settings, read once from environment variables. Secrets never live in the repo."""

import os
from dataclasses import dataclass
from zoneinfo import ZoneInfo


def _bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def normalize_db_url(url: str) -> str:
    # Hosts such as Render and Railway hand out postgres:// URLs; SQLAlchemy wants a driver.
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]
    if url.startswith("postgresql://"):
        url = "postgresql+psycopg://" + url[len("postgresql://"):]
    return url


@dataclass(frozen=True)
class Settings:
    env: str
    database_url: str
    secret_key: str
    cookie_secure: bool
    session_max_age: int
    display_tz: ZoneInfo
    lockout_threshold: int = 10
    lockout_minutes: int = 15

    @property
    def is_dev(self) -> bool:
        return self.env in {"dev", "test"}


def load_settings() -> Settings:
    env = os.getenv("APP_ENV", "production").lower()
    secret = os.getenv("SECRET_KEY", "")
    if not secret:
        if env not in {"dev", "test"}:
            raise RuntimeError("SECRET_KEY must be set outside dev/test")
        secret = "dev-only-insecure-secret"
    return Settings(
        env=env,
        database_url=normalize_db_url(os.getenv("DATABASE_URL", "sqlite:///./dev.db")),
        secret_key=secret,
        cookie_secure=_bool("COOKIE_SECURE", env not in {"dev", "test"}),
        session_max_age=int(os.getenv("SESSION_MAX_AGE", str(14 * 24 * 3600))),
        display_tz=ZoneInfo(os.getenv("DISPLAY_TZ", "Asia/Kuala_Lumpur")),
    )


settings = load_settings()
