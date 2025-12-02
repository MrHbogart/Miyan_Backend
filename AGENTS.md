# Repository Guidelines

## Project Structure & Module Organization
- `config/` holds Django settings, URLs, and ASGI/WSGI entry points; `.env` loads by default unless `DJANGO_SKIP_DOTENV=1`.
- `core/` has shared models, serializers, viewsets, and management commands; domain apps live in `miyanBeresht/`, `miyanGroup/`, and `miyanMadi/` with standard `models.py`/`serializers.py`/`views.py`/`urls.py`.
- `manage.py` is the CLI entry; `docker-compose.yml`/`docker-entrypoint.sh` support container runs; `tests/` holds pytest suites (healthcheck/menu APIs).
- Static/media paths and logging live in `config/settings.py`; secrets (keys, hosts, database, Sentry) come from environment variables.

## Build, Test, and Development Commands
- `make install` — install dependencies.
- `make lint` — run `ruff check` over `config core miyanBeresht miyanGroup miyanMadi tests`.
- `make test` — run pytest with `DJANGO_SETTINGS_MODULE=config.settings`; add `-k <pattern>` for focused runs.
- `make migrate` / `make collectstatic` — apply schema changes and gather static assets.
- `make runserver` — start Django at `0.0.0.0:8000`; `make shell` opens a Django shell; `docker-compose up --build` brings up the stack.

## Coding Style & Naming Conventions
- Python 3, PEP 8, 4-space indents; add type hints when practical.
- Snake_case for modules/functions/variables, PascalCase for classes; keep app file names aligned across urls/serializers/models/views.
- Run `make lint` before pushing; fix Ruff findings rather than ignoring rules.
- Name migrations descriptively (e.g., `0005_add_menu_flag.py`); align serializer and view names with their model/entity.

## Testing Guidelines
- Tests live in `tests/` and follow `test_*.py` with functions/methods named `test_*`.
- Prefer API-level tests for endpoints and serializer tests for business rules.
- Set `DJANGO_TEST=1` when needed for test-specific settings; cover both happy-path and failure cases for new endpoints.
- Always run `make test` (and `make lint`) before opening a pull request.

## Commit & Pull Request Guidelines
- Follow the existing history: short, present-tense summaries (e.g., `fix menu serializer image urls`); include scope or module when helpful.
- Squash noisy work-in-progress commits locally; reference issue IDs in the body if applicable.
- PRs should describe intent, notable design choices, migrations, and any manual verification (commands run, sample requests/responses). Attach screenshots or curl examples for API changes where useful.
- Keep branches rebased; avoid committing secrets or local `.env` files.

## Security & Configuration Tips
- Required env vars include `DJANGO_SECRET_KEY`, `DATABASE_URL` (via `dj_database_url`), `DJANGO_ALLOWED_HOSTS`, and optional `SENTRY_DSN`; never commit them.
- For local debug defaults, rely on `.env`; disable auto-loading in CI with `DJANGO_SKIP_DOTENV=1`.
- Treat media/static paths carefully in production; confirm storage backends and logging levels via `config/settings.py` before deploying.
