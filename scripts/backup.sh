#!/bin/sh
# Nightly backup: pg_dump -> gzip -> (optional) GPG encryption -> local dir and/or S3-compatible bucket.
# Keeps 30 days. Run it from a scheduler that can reach the database (host cron job, Render/Railway
# cron service, Fly scheduled machine, or crontab on a VPS):
#
#   0 18 * * *  /app/scripts/backup.sh     # 18:00 UTC = 02:00 Malaysia time
#
# Environment:
#   DATABASE_URL        required (postgres://... or postgresql://...)
#   BACKUP_DIR          local folder for dumps (default /backups)
#   BACKUP_PASSPHRASE   if set, dumps are encrypted with gpg --symmetric (AES256)
#   BACKUP_S3_URI       optional, e.g. s3://my-bucket/course-tracker (needs the aws CLI)
#   AWS_ENDPOINT_URL    optional, for Cloudflare R2 / Backblaze B2 / other S3-compatible storage
#   RETENTION_DAYS      default 30
set -eu

: "${DATABASE_URL:?DATABASE_URL is required}"
BACKUP_DIR="${BACKUP_DIR:-/backups}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
# pg_dump doesn't understand SQLAlchemy driver suffixes.
PG_URL="$(printf '%s' "$DATABASE_URL" | sed -e 's#^postgresql+psycopg://#postgresql://#' -e 's#^postgres://#postgresql://#')"

mkdir -p "$BACKUP_DIR"
FILE="$BACKUP_DIR/course-tracker-$STAMP.dump"

# Custom format (-Fc) is compressed and restores with pg_restore.
pg_dump --format=custom --no-owner --no-privileges --dbname="$PG_URL" --file="$FILE"

if [ -n "${BACKUP_PASSPHRASE:-}" ]; then
  printf '%s' "$BACKUP_PASSPHRASE" | gpg --batch --yes --quiet --pinentry-mode loopback \
    --passphrase-fd 0 --symmetric --cipher-algo AES256 --output "$FILE.gpg" "$FILE"
  rm -f "$FILE"
  FILE="$FILE.gpg"
fi

echo "Backup written: $FILE ($(du -h "$FILE" | cut -f1))"

if [ -n "${BACKUP_S3_URI:-}" ]; then
  ENDPOINT_ARGS=""
  [ -n "${AWS_ENDPOINT_URL:-}" ] && ENDPOINT_ARGS="--endpoint-url $AWS_ENDPOINT_URL"
  # shellcheck disable=SC2086
  aws s3 cp $ENDPOINT_ARGS "$FILE" "$BACKUP_S3_URI/$(basename "$FILE")"
  echo "Uploaded to $BACKUP_S3_URI"
  # Remote retention: set a 30-day lifecycle rule on the bucket (documented in README).
fi

find "$BACKUP_DIR" -name 'course-tracker-*.dump*' -type f -mtime +"$RETENTION_DAYS" -print -delete
