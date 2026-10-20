#!/bin/sh
# Restore a backup into a database (ideally a fresh, empty one).
#
#   TARGET_DATABASE_URL=postgresql://... scripts/restore.sh backups/course-tracker-20261020T180000Z.dump[.gpg]
#
# Encrypted dumps (.gpg) need BACKUP_PASSPHRASE. The target URL is deliberately a different variable
# from DATABASE_URL so you can't overwrite production by accident.
set -eu

FILE="${1:?usage: restore.sh <backup file>}"
: "${TARGET_DATABASE_URL:?set TARGET_DATABASE_URL to the database to restore into}"
PG_URL="$(printf '%s' "$TARGET_DATABASE_URL" | sed -e 's#^postgresql+psycopg://#postgresql://#' -e 's#^postgres://#postgresql://#')"

case "$FILE" in
  *.gpg)
    : "${BACKUP_PASSPHRASE:?BACKUP_PASSPHRASE is required for .gpg files}"
    PLAIN="$(mktemp)"
    trap 'rm -f "$PLAIN"' EXIT
    printf '%s' "$BACKUP_PASSPHRASE" | gpg --batch --yes --quiet --pinentry-mode loopback \
      --passphrase-fd 0 --decrypt --output "$PLAIN" "$FILE"
    FILE="$PLAIN"
    ;;
esac

pg_restore --clean --if-exists --no-owner --no-privileges --exit-on-error --dbname="$PG_URL" "$FILE"
echo "Restored. Check it with:"
echo "  psql \"$PG_URL\" -c 'select count(*) from episodes; select count(*) from status_events;'"
