# trixie ships postgresql-client 17, matching the Postgres 17 server (pg_dump must not be older)
FROM python:3.12-slim-trixie

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 PORT=8000

# postgresql-client gives pg_dump/pg_restore for scripts/backup.sh and restore.sh
RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client gnupg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app ./app
COPY migrations ./migrations
COPY alembic.ini ./
COPY scripts ./scripts
COPY course ./course

RUN useradd --create-home --uid 10001 tracker && chmod +x scripts/*.sh
USER tracker

EXPOSE 8000
# Apply migrations, then serve. --proxy-headers trusts the host's TLS-terminating proxy.
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --proxy-headers --forwarded-allow-ips='*'"]
