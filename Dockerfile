FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x scripts/docker-entrypoint.sh && \
    addgroup --system miyan && adduser --system --ingroup miyan miyan && \
    chown -R miyan:miyan /app

USER miyan

EXPOSE 8002

ENTRYPOINT ["./scripts/docker-entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8002", "--workers", "3", "--timeout", "120"]
