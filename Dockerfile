FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    APP_HOME=/home/miyan/Miyan_Backend

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip && pip wheel --wheel-dir=/wheels -r requirements.txt

FROM python:3.11-slim

ARG APP_UID=1000
ARG APP_GID=1000

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    APP_HOME=/home/miyan/Miyan_Backend \
    APP_USER=miyan \
    APP_GROUP=miyan

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    gosu \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /wheels /wheels
RUN pip install --upgrade pip && pip install /wheels/* && rm -rf /wheels

COPY . .
RUN set -eux; \
    chmod +x scripts/docker-entrypoint.sh; \
    addgroup --system --gid ${APP_GID} ${APP_GROUP} 2>/dev/null || true; \
    id -u ${APP_USER} >/dev/null 2>&1 || \
        adduser --system --home ${APP_HOME} --uid ${APP_UID} --ingroup ${APP_GROUP} ${APP_USER}; \
    mkdir -p ${APP_HOME}/staticfiles ${APP_HOME}/media

EXPOSE 8002

ENTRYPOINT ["./scripts/docker-entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8002", "--workers", "3", "--timeout", "120"]
