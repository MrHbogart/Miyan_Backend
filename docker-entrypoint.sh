#!/usr/bin/env sh
set -euo pipefail

# Allow overriding the command but always ensure migrations and static files are ready.
python manage.py collectstatic --clear --noinput
python - <<'PY'
import os
import time

import django
from django.db import connections
from django.db.utils import OperationalError

django.setup()

timeout = int(os.environ.get('DB_WAIT_TIMEOUT', '60'))
interval = max(1, int(os.environ.get('DB_WAIT_INTERVAL', '2')))
deadline = time.monotonic() + timeout
connection = connections['default']

while True:
    try:
        connection.ensure_connection()
        connection.close()
        break
    except OperationalError as exc:
        if time.monotonic() >= deadline:
            raise RuntimeError('Database is unavailable') from exc
        time.sleep(interval)
PY
python - <<'PY'
from pathlib import Path
import os
import shutil

from django.conf import settings

static_root = Path(settings.STATIC_ROOT)
static_root.mkdir(parents=True, exist_ok=True)
Path(static_root, '.static_collected').write_text('collected')

def set_permissions(root: Path) -> None:
    for current, dirs, files in os.walk(root):
        os.chmod(current, 0o755)
        for name in files:
            os.chmod(Path(current) / name, 0o644)

def copy_static(target: Path) -> None:
    if target.exists():
        if target.is_symlink() or target.is_file():
            target.unlink()
        else:
            shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(static_root, target)
    set_permissions(target)

set_permissions(static_root)

copy_static(Path(settings.BASE_DIR) / 'static')
copy_static(Path(settings.BASE_DIR) / 'public' / 'static')
PY
python manage.py migrate --noinput

exec "$@"
