#!/usr/bin/env sh
set -euo pipefail

umask 0022

APP_USER="${APP_USER:-django}"
STATIC_ROOT="${DJANGO_STATIC_ROOT:-/app/staticfiles}"
MEDIA_ROOT="${DJANGO_MEDIA_ROOT:-/app/media}"

log() {
    printf '[entrypoint] %s\n' "$*"
}

run_as_app() {
    if [ "$(id -u)" = "0" ]; then
        gosu "${APP_USER}:${APP_USER}" "$@"
    else
        "$@"
    fi
}

prepare_directories() {
    mkdir -p "${STATIC_ROOT}" "${MEDIA_ROOT}" "${MEDIA_ROOT}/menu_items/gifs"
    if [ "$(id -u)" = "0" ]; then
        chown -R "${APP_USER}:${APP_USER}" "${STATIC_ROOT}" "${MEDIA_ROOT}" /app
    fi
}

wait_for_db() {
    run_as_app python <<'PY'
import os
import time
import django
from django.db import connections
from django.db.utils import OperationalError

django.setup()
timeout = int(os.environ.get('DB_WAIT_TIMEOUT', '60'))
interval = max(1, int(os.environ.get('DB_WAIT_INTERVAL', '2')))
deadline = time.monotonic() + timeout
conn = connections['default']
while True:
    try:
        conn.ensure_connection()
        conn.close()
        break
    except OperationalError as exc:
        if time.monotonic() >= deadline:
            raise RuntimeError('Database is unavailable') from exc
        time.sleep(interval)
PY
}

log "Preparing static and media directories..."
prepare_directories

log "Preparing migration state..."
# In development we remove existing migration files so the container always
# generates fresh migrations at startup. This avoids stale migration conflicts
# during active development. Do NOT enable this in production — keep migrations
# in version control there.
log "Removing any existing migration files so startup creates fresh migrations (development only)"
run_as_app sh -c "find . -path '*/migrations/*.py' -not -name '__init__.py' -delete || true"
run_as_app sh -c "find . -path '*/migrations/*.pyc' -delete || true"

# Create new migration files for each app. We do this before waiting for the DB
# so `makemigrations` can run even if the DB is not yet reachable.
run_as_app python manage.py makemigrations core miyanBeresht miyanMadi miyanGroup --noinput || \
    log "makemigrations returned non-zero exit code; continuing because DB may be unavailable yet"

log "Waiting for database..."
wait_for_db

log "Applying database migrations (app-by-app to avoid dependency order issues)..."
# Apply migrations app-by-app in an explicit order so dependent models are created
# in a deterministic sequence. If an app has no migrations generated, migrate will
# simply do nothing.
run_as_app python manage.py migrate core --noinput || log "migrate core failed"
run_as_app python manage.py migrate miyanBeresht --noinput || log "migrate miyanBeresht failed"
run_as_app python manage.py migrate miyanMadi --noinput || log "migrate miyanMadi failed"
run_as_app python manage.py migrate miyanGroup --noinput || log "migrate miyanGroup failed"
# Finally ensure any remaining migrations (including auth, contenttypes, sessions)
# are applied.
run_as_app python manage.py migrate --noinput || log "final migrate failed"

log "Collecting static assets..."
run_as_app python manage.py collectstatic --noinput

log "Starting Gunicorn..."
if [ "$(id -u)" = "0" ]; then
    exec gosu "${APP_USER}:${APP_USER}" "$@"
else
    exec "$@"
fi
