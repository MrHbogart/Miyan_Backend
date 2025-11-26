# Mian Backend (Django + DRF)

This repository contains the Django REST API for the Miyan platform. The service now runs **only on PostgreSQL** whether you are in development or production, and all sensitive settings come from `.env` files so they can be shared between Docker, virtualenvs, and any CI pipelines.

## Quick start (local development)

1. Copy the provided defaults and edit secrets/domains to match your environment:

   ```bash
   cd Miyan_Backend
   cp .env.example .env
   # update DJANGO_SECRET_KEY, database credentials, etc.
   ```

   The example file already whitelists `miyangroup.com` and `www.miyangroup.com` alongside localhost origins so it can be used for nginx on the production domains.

   To rotate credentials, rely on Django's built-in helpers so secrets are always production grade:

   ```bash
   # Requires Django dependencies (install locally or run inside the backend container)
   python - <<'PY'
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   PY

   # Generate a strong database password (safe for .env files)
   python - <<'PY'
   import secrets
   print(secrets.token_urlsafe(32))
   PY
   ```

2. (Optional) create a virtual environment and install the dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements-dev.txt  # or run `make install-dev`
   ```

3. Decide which database to use locally:

   - **SQLite (default):** remove/comment the `DATABASE_URL` and `POSTGRES_*` lines from `.env`. The local settings automatically fall back to `db.sqlite3`.
   - **PostgreSQL:** leave the default values or point them at your local Postgres instance.

4. Run the standard Django workflow:

   ```bash
   python manage.py migrate
   python manage.py runserver 0.0.0.0:8002
   ```

   The admin UI is reachable at `http://127.0.0.1:8002/admin/` once you create a superuser (`python manage.py createsuperuser`).

5. Run linting/tests locally to match CI:

   ```bash
   make lint
   make test
   ```

## Docker deployment

A production-focused Docker stack now ships with the repository:

```bash
docker compose up --build -d
```

- `backend` — builds the Django/Gunicorn image, waits for Postgres, runs migrations, collects static files, and finally serves on port `8002` (so nginx can proxy `/api/`).
- `db` — PostgreSQL 15 with persistent volume storage.

Important commands:

```bash
# Run one-off Django management commands
docker compose run --rm backend python manage.py shell

# Create new migrations from model changes
docker compose run --rm backend python manage.py makemigrations

# Apply migrations manually (entrypoint already runs this on startup)
docker compose run --rm backend python manage.py migrate
```

Static files live in the `static_volume` named volume and uploaded media in `media_volume`. Mount them to host paths if you want to back them up externally.

### Security defaults

- The runtime image runs as a non-root user with a read-only filesystem and health checks hitting `/api/core/health/`.
- `config/settings.py` enforces secure cookies, HSTS, and fails fast if `DJANGO_SECRET_KEY` is missing while `DJANGO_DEBUG=False`.
- Throttling is enabled in DRF to guard API abuse; tune via `DRF_*` environment variables.
- `scripts/docker-entrypoint.sh` now runs `python manage.py check --deploy --fail-level WARNING` on container start.

### Observability & monitoring

- Structured JSON logs are emitted to stdout (capturable by Docker, journald, Cloud Logging, etc.).
- Optional Sentry integration (`SENTRY_DSN` & friends) captures errors and traces.
- `/api/core/health/` returns deployment metadata (`version`, `revision`, timestamp) for uptime monitoring and Docker health checks.

### Local quality & CI

- Development tooling lives in `requirements-dev.txt` and is wired via a `Makefile`.
- `make check` (lint + tests) mirrors the GitHub Actions workflow defined in `.github/workflows/ci.yml`.
- Pytest + coverage ensure the critical endpoints (starting with the healthcheck) stay online.

### CI/CD automation

- `.github/workflows/ci.yml` now also contains a `deploy` job that runs on a self-hosted runner labelled `self-hosted, linux, production` whenever changes hit `main`.
- The deploy job stops the existing stack, rebuilds the Docker services, and restarts them with the current `APP_VERSION` and `APP_COMMIT_SHA`.
- Follow `todo.md` for the exact runner installation steps and any remaining manual tasks required to finish the pipeline.

### Settings profiles

The project now relies on a single settings module (`config/settings.py`) for every
environment—flip the behavior using environment variables (`DJANGO_DEBUG`, `DATABASE_URL`,
etc.). `config/settings.production` remains only as a backwards-compatible shim so existing
deployments that import `config.settings.production` continue to work; it simply forces
`DJANGO_DEBUG=0` and reuses the main settings module. There is no longer a need to copy files
before running Docker Compose.

## Environment variables

Key settings supported by the backend:

| Variable | Description |
| --- | --- |
| `APP_VERSION` / `APP_COMMIT_SHA` | Metadata returned by the healthcheck for traceability. |
| `DJANGO_SECRET_KEY` | Required cryptographic secret. |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hosts (already defaults to `miyangroup.com` variants). |
| `DJANGO_CORS_ALLOWED_ORIGINS` / `DJANGO_CSRF_TRUSTED_ORIGINS` | Origins for SSR frontend + nginx (`https://miyangroup.com`). |
| `DJANGO_SESSION_COOKIE_NAME` / `DJANGO_CSRF_COOKIE_NAME` | Override cookie names if running multiple Django apps under same domain. |
| `DATABASE_URL` | Preferred way to point Django at PostgreSQL (`postgres://user:pass@db:5432/name`). |
| `POSTGRES_*` | Used when `DATABASE_URL` is not provided (handy inside docker-compose). |
| `DJANGO_SECURE_SSL_REDIRECT`, `DJANGO_TRUST_PROXY_HEADERS` | Toggle SSL + proxy aware headers for nginx/Certbot deployments. |
| `DRF_USER_THROTTLE_RATE` / `DRF_ANON_THROTTLE_RATE` | Rate limit strings consumed by DRF's throttling system (e.g., `1000/hour`). |
| `SENTRY_DSN`, `SENTRY_ENVIRONMENT`, `SENTRY_TRACES_SAMPLE_RATE`, `SENTRY_PROFILES_SAMPLE_RATE` | Configure Sentry error + performance monitoring. |

Anything set in `.env` is automatically loaded by `config/settings.py`, so running with `DJANGO_DEBUG=False` locally or in Docker is safe—the admin panel still works because static files are served via WhiteNoise even in containerized mode.
