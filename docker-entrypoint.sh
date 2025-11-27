#!/usr/bin/env sh
set -euo pipefail

# Allow overriding the command but always ensure migrations and static files are ready.
python manage.py collectstatic --clear --noinput
python - <<'PY'
from pathlib import Path
import shutil

from django.conf import settings

static_root = Path(settings.STATIC_ROOT)
static_root.mkdir(parents=True, exist_ok=True)
Path(static_root, '.static_collected').write_text('collected')

def copy_static(target: Path) -> None:
    if target.exists():
        if target.is_symlink() or target.is_file():
            target.unlink()
        else:
            shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(static_root, target)

copy_static(Path(settings.BASE_DIR) / 'static')
copy_static(Path(settings.BASE_DIR) / 'public' / 'static')
PY
python manage.py migrate --noinput

exec "$@"
