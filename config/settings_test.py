"""Test settings that keep the suite isolated from Docker/Postgres dependencies."""

import os

os.environ.setdefault('DJANGO_SKIP_DOTENV', '1')
os.environ.setdefault('DJANGO_TEST', '1')

from .settings import *  # noqa: F401,F403
