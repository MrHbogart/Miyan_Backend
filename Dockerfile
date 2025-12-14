FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VENV_PATH="/opt/venv"

WORKDIR /app

RUN python -m venv ${VENV_PATH}
ENV PATH="${VENV_PATH}/bin:${PATH}"

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim AS final

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings \
    VENV_PATH="/opt/venv" \
    APP_USER="django" \
    APP_HOME="/home/django"

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gosu curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder ${VENV_PATH} ${VENV_PATH}
ENV PATH="${VENV_PATH}/bin:${PATH}"

COPY . .

RUN set -eux; \
    groupadd --system "${APP_USER}" || true; \
    useradd --system --gid "${APP_USER}" --home "${APP_HOME}" --shell /bin/bash "${APP_USER}" || true; \
    mkdir -p "${APP_HOME}" /app/staticfiles /app/media; \
    chown -R "${APP_USER}:${APP_USER}" "${APP_HOME}" /app "${VENV_PATH}"; \
    chmod +x /app/docker-entrypoint.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--threads", "2", "--log-file", "-"]
