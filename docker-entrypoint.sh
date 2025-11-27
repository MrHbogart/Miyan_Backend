#!/usr/bin/env sh
set -euo pipefail

# Allow overriding the command but always ensure migrations and static files are ready.
python manage.py collectstatic --clear --noinput
python - <<'PY'
from pathlib import Path
from django.conf import settings

static_root = Path(settings.STATIC_ROOT)
static_root.mkdir(parents=True, exist_ok=True)
Path(static_root, '.static_collected').write_text('collected')

def ensure_link(alias_path: Path) -> None:
    if alias_path.exists() and not alias_path.is_symlink():
        return
    alias_path.parent.mkdir(parents=True, exist_ok=True)
    if alias_path.is_symlink():
        alias_path.unlink()
    alias_path.symlink_to(static_root, target_is_directory=True)

ensure_link(Path(settings.BASE_DIR) / 'static')
ensure_link(Path(settings.BASE_DIR) / 'public' / 'static')
PY
python manage.py migrate --noinput

exec "$@"
