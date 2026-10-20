# Course Tracker

A private, single-user web app for logging progress through the AI engineering course: episode
status with full history, module checklists, study time, production time, a dashboard, and
export. This is the MVP from the Course Tracker PRD (20 Oct 2026).

Stack: FastAPI · Jinja2 + HTMX · PostgreSQL (SQLite for local dev/tests) · Alembic · Argon2 · pytest · Docker.

## Run locally (no Docker)

```bash
py -3.12 -m venv .venv
.venv/Scripts/pip install -r requirements-dev.txt     # macOS/Linux: .venv/bin/pip
cp .env.example .env                                   # then set SECRET_KEY
```

PowerShell, from the project folder:

```powershell
$env:APP_ENV="dev"; $env:COOKIE_SECURE="false"
.venv\Scripts\alembic upgrade head
.venv\Scripts\python -m app.cli create-owner --email you@example.com
.venv\Scripts\python -m app.cli import-course course\AI_Engineering_Course_Razeen_v7.md
.venv\Scripts\uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000 and sign in. (You can also import the course from Settings instead of the CLI.)

## Run locally with Docker + Postgres

```bash
docker compose up --build -d
docker compose exec app python -m app.cli create-owner --email you@example.com
docker compose exec app python -m app.cli import-course course/AI_Engineering_Course_Razeen_v7.md
```

## Tests

```bash
.venv/Scripts/python -m pytest                     # SQLite
TEST_DATABASE_URL=postgresql+psycopg://... pytest  # against Postgres (what CI does)
```

CI (`.github/workflows/ci.yml`) runs the suite on Postgres and SQLite, runs `pip-audit` on the
pinned dependencies, and builds the Docker image on every push.

## Admin commands

There is no sign-up page. Accounts are managed on the server:

| Command | What it does |
|---|---|
| `python -m app.cli create-owner --email X` | Creates the one owner account (prompts for a 12+ char password) |
| `python -m app.cli reset-password --email X` | New password, signs out all sessions, clears lockout |
| `python -m app.cli unlock --email X` | Clears a 15-minute lockout early |
| `python -m app.cli import-course FILE [--label v7]` | Loads the course markdown |

## Deploy to Vercel (free Hobby plan)

Vercel runs the app as a serverless function and Neon (added from Vercel's Storage tab)
provides Postgres. Every push to `main` redeploys, and each build runs `alembic upgrade head`
first (see `pyproject.toml`).

1. **Import the repo.** On vercel.com, sign in with GitHub → *Add New… → Project* → import
   `ai-engineering-course-tracker`. Leave the framework as detected (FastAPI). Don't deploy yet
   if it offers; if it deploys and fails, that's expected until steps 2–3 are done.
2. **Add a database.** In the project: *Storage → Create Database → Neon (Postgres)* → region
   Singapore (closest to Malaysia) → connect it to the project for all environments. This sets
   `DATABASE_URL` for you.
3. **Add settings.** *Settings → Environment Variables*, for Production and Preview:
   - `SECRET_KEY`: a long random string (`python -c "import secrets; print(secrets.token_urlsafe(48))"`)
   - `APP_ENV` = `production`
4. **Deploy.** *Deployments → Redeploy*. The build log should show
   `Running upgrade -> 0001, initial schema`.
5. **Create your login** (once, from your computer). Copy the Neon connection string from
   *Storage → your database → .env.local tab* and run in PowerShell from this folder:
   ```powershell
   $env:APP_ENV="production"; $env:SECRET_KEY="anything"; $env:DATABASE_URL="<paste the Neon URL>"
   .venv\Scripts\python -m app.cli create-owner --email you@example.com
   ```
   It asks for your password twice (12+ characters).
6. **Sign in** at your `*.vercel.app` address → *Settings* → upload
   `course/AI_Engineering_Course_Razeen_v7.md` → *Import course*.
7. **Turn on nightly backups.** On GitHub: repo *Settings → Secrets and variables → Actions →
   New repository secret*, add `BACKUP_DATABASE_URL` (Neon's **unpooled** connection string) and
   `BACKUP_PASSPHRASE` (20+ random characters, saved in your password manager). Then *Actions →
   Nightly backup → Run workflow* to test it. Backups are encrypted because anyone signed in to
   GitHub can download artifacts from a public repo.

Trade-offs versus a container host: the first request after a quiet spell is slower (cold
start), and the database is reachable over the internet (protected by its password and TLS)
rather than private to the host. Neon also keeps its own short point-in-time history you can
restore from in its console.

To restore a GitHub backup: download the artifact from the workflow run, unzip it, and follow
*Backups and restore* below with `BACKUP_PASSPHRASE` set.

## Deploying to a container host

Any container host works (Render, Fly.io, Railway, or a small VPS). Check current pricing first.

1. Create a managed Postgres database (Neon production runs Postgres 18; the Docker image ships pg_dump 17, so run backups from the GitHub workflow or upgrade the client). Keep it private to the host's network if the host allows that.
2. Deploy this repo's Dockerfile. The container runs `alembic upgrade head` on start.
3. Set environment variables in the host dashboard, never in the repo:
   - `DATABASE_URL`: the host's Postgres URL (`postgres://` URLs are accepted)
   - `SECRET_KEY`: `python -c "import secrets; print(secrets.token_urlsafe(48))"`
   - `APP_ENV=production` (`COOKIE_SECURE` defaults to true, so the site must be served over HTTPS)
4. Open a shell on the host and run `create-owner` and `import-course`.

Security built in: Argon2id password hashes; a 15-minute lockout after 10 failed sign-ins;
signed session cookies with `Secure`, `HttpOnly` and `SameSite=Lax`; a CSRF token on every POST;
a strict Content-Security-Policy (no inline scripts, no third-party scripts, htmx is vendored);
HSTS; `noindex`; no analytics. A password change signs out every other session.

## Backups and restore

`scripts/backup.sh` runs `pg_dump` (custom format), optionally encrypts the dump with GPG, writes
it to `BACKUP_DIR`, optionally uploads it to S3-compatible storage (Cloudflare R2, Backblaze B2,
AWS S3), and deletes local dumps older than 30 days.

**Nightly schedule.** Run it from something inside the host that can reach the database:

- VPS: `crontab -e` → `0 18 * * * cd /srv/course-tracker && docker compose exec -T app scripts/backup.sh`
  (18:00 UTC is 02:00 Malaysia time)
- Render / Railway: a cron job service using this image, command `scripts/backup.sh`, schedule `0 18 * * *`
- Fly.io: a scheduled machine (`fly machine run . --schedule daily --command scripts/backup.sh`)

For off-host storage set `BACKUP_S3_URI` (plus `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and,
for R2/B2, `AWS_ENDPOINT_URL`) and add a 30-day lifecycle rule on the bucket. The image doesn't
include the `aws` CLI; add `pip install awscli` to the Dockerfile if you use S3 upload. Set
`BACKUP_PASSPHRASE` so dumps are encrypted before they leave the host, and keep the passphrase in
your password manager: without it the backups can't be restored.

**Restore (do this once before calling the MVP done):**

1. Create a fresh, empty Postgres database (locally: `docker run -d --name restore-test -e POSTGRES_PASSWORD=x -p 5433:5432 postgres:17`).
2. Download the latest dump from your storage.
3. Restore into it:
   ```bash
   TARGET_DATABASE_URL=postgresql://postgres:x@localhost:5433/postgres \
   BACKUP_PASSPHRASE=... scripts/restore.sh course-tracker-20261020T180000Z.dump.gpg
   ```
4. Check the counts it prints, then point a local copy of the app at it
   (`DATABASE_URL=... uvicorn app.main:app`) and sign in to confirm your progress is there.
5. Write the date you tested it here: _not yet tested_.

The JSON and CSV exports in Settings are a second, host-independent copy of your data.

## Project layout

```
app/
  main.py         app factory, middleware, error handlers
  config.py       settings from environment variables
  models.py       tables (progress keyed by stable episode_key / module_key)
  importer.py     course markdown parser and loader
  security.py     Argon2, lockout, sessions, CSRF
  services.py     queries and updates used by the pages
  export.py       JSON / CSV export
  cli.py          admin commands
  routes/         auth, episodes (+ dashboard), modules (+ study log), settings (+ export)
  templates/      Jinja2 pages and HTMX partials
  static/         CSS, htmx (vendored), app.js
migrations/       Alembic
scripts/          backup.sh, restore.sh
course/           the v7 course markdown
tests/
```

## Not in the MVP (per the PRD)

Two-factor sign-in, version upgrades with title matching, script drafts, per-platform links, view
counts, the failure log, the pace chart and the weekly review are v1. The `script_markdown` and
`totp_secret` columns already exist so v1 doesn't need to change those tables.
