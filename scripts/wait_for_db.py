"""Simple Postgres waiting helper for Dockerized deployments."""

from __future__ import annotations

import os
import time
from urllib.parse import urlparse

import psycopg2


def _get_db_params() -> dict[str, str | int | None]:
    url = os.getenv("DATABASE_URL")
    if url:
        parsed = urlparse(url)
        return {
            "dbname": (parsed.path or "/").lstrip("/"),
            "user": parsed.username,
            "password": parsed.password,
            "host": parsed.hostname,
            "port": parsed.port or 5432,
        }

    return {
        "dbname": os.getenv("POSTGRES_DB", "postgres"),
        "user": os.getenv("POSTGRES_USER", "postgres"),
        "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "host": os.getenv("POSTGRES_HOST", "db"),
        "port": int(os.getenv("POSTGRES_PORT", "5432")),
    }


def wait_for_db(max_attempts: int = 30, sleep_seconds: int = 2) -> None:
    params = _get_db_params()
    attempt = 0
    while True:
        try:
            with psycopg2.connect(**params):
                return
        except psycopg2.OperationalError:
            attempt += 1
            if attempt >= max_attempts:
                raise
            time.sleep(sleep_seconds)


if __name__ == "__main__":
    wait_for_db()
