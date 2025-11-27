#!/usr/bin/env sh
set -euo pipefail

# Allow overriding the command but always ensure migrations and static files are ready.
python manage.py collectstatic --clear --noinput
python manage.py migrate --noinput

exec "$@"
