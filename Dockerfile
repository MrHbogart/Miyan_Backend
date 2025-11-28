FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VENV_PATH="/opt/venv"

WORKDIR /app

RUN python -m venv ${VENV_PATH}
ENV PATH="${VENV_PATH}/bin:${PATH}"

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

FROM python:3.11-slim AS final

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings \
    PATH="/opt/venv/bin:${PATH}"

WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY . .

# Create an unprivileged user to run the app
RUN set -eux; \
    groupadd --system miyan || true; \
    useradd --system --gid miyan --home /home/miyan --shell /bin/sh miyan || true; \
    mkdir -p /home/miyan; \
    chown -R miyan:miyan /home/miyan /app /opt/venv; \
    chmod -R go-rwx /opt/venv

RUN chmod +x docker-entrypoint.sh

ENV HOME=/home/miyan

USER miyan

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--threads", "2", "--log-file", "-"]
