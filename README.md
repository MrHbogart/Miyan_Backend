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

2. (Optional) create a virtual environment and install the dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Provision PostgreSQL (either via Docker, Homebrew, etc.) and ensure the credentials in `.env` match. Then run the standard Django workflow:

   ```bash
   python manage.py migrate
   python manage.py runserver 0.0.0.0:8000
   ```

   The admin UI is reachable at `http://127.0.0.1:8000/admin/` once you create a superuser (`python manage.py createsuperuser`).

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

## Environment variables

Key settings supported by the backend:

| Variable | Description |
| --- | --- |
| `DJANGO_SECRET_KEY` | Required cryptographic secret. |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hosts (already defaults to `miyangroup.com` variants). |
| `DJANGO_CORS_ALLOWED_ORIGINS` / `DJANGO_CSRF_TRUSTED_ORIGINS` | Origins for SSR frontend + nginx (`https://miyangroup.com`). |
| `DATABASE_URL` | Preferred way to point Django at PostgreSQL (`postgres://user:pass@db:5432/name`). |
| `POSTGRES_*` | Used when `DATABASE_URL` is not provided (handy inside docker-compose). |
| `DJANGO_SECURE_SSL_REDIRECT`, `DJANGO_TRUST_PROXY_HEADERS` | Toggle SSL + proxy aware headers for nginx/Certbot deployments. |

Anything set in `.env` is automatically loaded by `config/settings.py`, so running with `DJANGO_DEBUG=False` locally or in Docker is safe—the admin panel still works because static files are served via WhiteNoise even in containerized mode.
