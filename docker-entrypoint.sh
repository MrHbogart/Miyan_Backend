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

log "Checking for new migrations..."
run_as_app python manage.py makemigrations core miyanBeresht miyanMadi miyanGroup inventory --noinput

log "Waiting for database..."
wait_for_db

log "Applying database migrations..."
run_as_app python manage.py migrate --noinput

log "Collecting static assets..."
run_as_app python manage.py collectstatic --noinput

log "Starting Gunicorn..."
if [ "$(id -u)" = "0" ]; then
    exec gosu "${APP_USER}:${APP_USER}" "$@"
else
    exec "$@"
fi
