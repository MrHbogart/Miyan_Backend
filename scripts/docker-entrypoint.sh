#!/bin/bash
set -o errexit
set -o nounset
set -o pipefail

python scripts/wait_for_db.py
python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
