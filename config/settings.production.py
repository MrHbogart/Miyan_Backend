"""Thin production settings module kept for backwards compatibility.

Historically the deployment workflow required copying this file over
``config/settings.py`` to enable hardened settings. The main settings module
now handles both development and production based on environment variables,
but external tooling may still import ``config.settings.production``.  Rather
than duplicate a large configuration tree, we force ``DJANGO_DEBUG`` off and
reuse the canonical settings module.
"""

from __future__ import annotations

import os

os.environ.setdefault('DJANGO_DEBUG', '0')

from .settings import *  # noqa: F401,F403,E402
