#!/usr/bin/env sh
set -euo pipefail

## Entrypoint: run collectstatic, wait for DB, migrate, then exec
# Runs as the container user (created in the Dockerfile). When running in CI
# or build contexts as root these ops will still work because the build
# chowned the required directories to the app user.

umask 0022

echo "Collecting static files..."
python manage.py collectstatic --clear --noinput || true

echo "Waiting for DB to become available..."
python - <<'PY'
import os, time
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
        print('waiting-for-db', flush=True)
        conn.ensure_connection()
        conn.close()
        print('db-ready', flush=True)
        break
    except OperationalError as exc:
        if time.monotonic() >= deadline:
            raise RuntimeError('Database is unavailable') from exc
        time.sleep(interval)
PY

echo "Preparing static & media permissions..."
python - <<'PY'
from pathlib import Path
import os
import shutil
from django.conf import settings

static_root = Path(settings.STATIC_ROOT)
media_root = Path(settings.MEDIA_ROOT)

static_root.mkdir(parents=True, exist_ok=True)
media_root.mkdir(parents=True, exist_ok=True)

def set_permissions(root: Path) -> None:
    for current, dirs, files in os.walk(root):
        try:
            os.chmod(current, 0o755)
        except PermissionError:
            pass
        for name in files:
            try:
                os.chmod(Path(current) / name, 0o644)
            except PermissionError:
                pass

set_permissions(static_root)
set_permissions(media_root)
PY

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting process..."
exec "$@"
