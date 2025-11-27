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
PY
python manage.py migrate --noinput

exec "$@"
