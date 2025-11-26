"""Pytest configuration for deterministic local runs."""

import os

# Ensure Django doesn't try to load the docker-focused .env file and Postgres
# credentials during CI/local pytest runs where that infrastructure isn't
# available. This file lives at the project root so pytest imports it before
# Django loads settings.
os.environ.setdefault('DJANGO_SKIP_DOTENV', '1')
os.environ.setdefault('DJANGO_TEST', '1')
