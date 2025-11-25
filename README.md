# Mian Backend (Django + DRF)

This repository contains a Django REST Framework backend scaffolded for the Mian app. It uses SQLite for development and is prepared to be migrated to PostgreSQL later.

Quick start (macOS / zsh):

0. Configure environment variables (copy the example file and tweak as needed):

```bash
cp .env.example .env
# edit DJANGO_SECRET_KEY, allowed hosts, etc.
```

`DJANGO_DEBUG=True` (default in the example) keeps everything running locally with SQLite and HTTP.  
Setting `DJANGO_DEBUG=False` switches the app to PostgreSQL credentials from `.env` and enforces HTTPS-secure cookies for deployment behind gunicorn/nginx.

1. Create/activate virtualenv (already created in this workspace as `.venv`):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run migrations and start development server:

```bash
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

3. Admin access:

- URL: http://127.0.0.1:8000/admin/
- A default superuser `admin` with password `adminpass` was created by the setup script in this session. Change the password after first login.

API endpoints are exposed under `/api/` (browsable API available). JWT token endpoints:

- POST `/api/token/`  — obtain access and refresh tokens
- POST `/api/token/refresh/` — refresh access token

Notes:
- This is a development setup. Adjust `.env` before deploying (especially `DJANGO_ALLOWED_HOSTS`, `DJANGO_CORS_ALLOWED_ORIGINS`, Postgres credentials, etc.).
