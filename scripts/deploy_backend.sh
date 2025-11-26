#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: ./scripts/deploy_backend.sh [options]

Automates the standard backend deployment workflow inside /home/miyan/Miyan_Backend:
  docker compose pull
  docker compose build --no-cache
  docker compose up -d
  docker compose exec backend python manage.py migrate --noinput
  docker compose exec backend python manage.py collectstatic --noinput

Options:
  --use-cache          Allow Docker to use cached layers during the build.
  --skip-pull          Skip docker compose pull (useful for offline deploys).
  --follow-logs        Tail backend logs after startup (Ctrl+C to stop).
  --create-superuser   Run createsuperuser after migrations/collectstatic.
  -h, --help           Show this help message.
EOF
}

FOLLOW_LOGS=false
CREATE_SUPERUSER=false
USE_CACHE=false
SKIP_PULL=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --follow-logs)
      FOLLOW_LOGS=true
      ;;
    --create-superuser)
      CREATE_SUPERUSER=true
      ;;
    --use-cache)
      USE_CACHE=true
      ;;
    --skip-pull)
      SKIP_PULL=true
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
  shift
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "Working directory: ${REPO_DIR}"
cd "${REPO_DIR}"

if [[ "${SKIP_PULL}" == "false" ]]; then
  echo "==> Pulling latest images..."
  docker compose pull
else
  echo "==> Skipping docker compose pull."
fi

echo "==> Building backend image..."
if [[ "${USE_CACHE}" == "true" ]]; then
  docker compose build
else
  docker compose build --no-cache
fi

echo "==> Starting containers in detached mode..."
docker compose up -d

echo "==> Running migrations..."
docker compose exec backend python manage.py migrate --noinput

echo "==> Collecting static files..."
docker compose exec backend python manage.py collectstatic --noinput

if [[ "${CREATE_SUPERUSER}" == "true" ]]; then
  echo "==> Launching createsuperuser (follow prompts)..."
  docker compose exec backend python manage.py createsuperuser
fi

if [[ "${FOLLOW_LOGS}" == "true" ]]; then
  echo "==> Tailing backend logs (Ctrl+C to stop)..."
  docker compose logs -f backend
else
  echo "Deployment complete. Use 'docker compose logs -f backend' to inspect logs if needed."
fi
