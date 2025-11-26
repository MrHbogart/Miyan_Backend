#!/bin/bash
set -o errexit
set -o nounset
set -o pipefail

APP_HOME="${APP_HOME:-/home/miyan/Miyan_Backend}"
APP_USER="${APP_USER:-miyan}"
APP_GROUP="${APP_GROUP:-miyan}"
APP_UID="${APP_UID:-1000}"
APP_GID="${APP_GID:-1000}"
STATIC_DIR="${APP_HOME}/staticfiles"
MEDIA_DIR="${APP_HOME}/media"

current_uid() {
    id -u "${APP_USER}"
}

current_gid() {
    getent group "${APP_GROUP}" | cut -d: -f3
}

sync_ids() {
    if [ "$(current_gid)" != "${APP_GID}" ]; then
        groupmod -g "${APP_GID}" "${APP_GROUP}"
    fi

    if [ "$(current_uid)" != "${APP_UID}" ]; then
        usermod -u "${APP_UID}" -g "${APP_GID}" "${APP_USER}"
    fi
}

ensure_app_dirs() {
    mkdir -p "${STATIC_DIR}" "${MEDIA_DIR}"
    chown -R "${APP_USER}:${APP_GROUP}" "${STATIC_DIR}" "${MEDIA_DIR}"
}

run_as_app() {
    gosu "${APP_USER}:${APP_GROUP}" "$@"
}

sync_ids
ensure_app_dirs

run_as_app python scripts/wait_for_db.py
run_as_app python manage.py migrate --noinput
run_as_app python manage.py collectstatic --noinput
run_as_app python manage.py check --deploy --fail-level WARNING

exec gosu "${APP_USER}:${APP_GROUP}" "$@"
