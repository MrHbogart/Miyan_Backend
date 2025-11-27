.PHONY: install lint test migrate collectstatic runserver shell

PYTHON ?= python
PIP ?= $(PYTHON) -m pip
MANAGE := $(PYTHON) manage.py

install:
\t$(PIP) install --upgrade pip
\t$(PIP) install -r requirements.txt
\t$(PIP) install -r requirements-dev.txt

lint:
\t$(PYTHON) -m ruff check config core miyanBeresht miyanGroup miyanMadi tests

test:
\tDJANGO_SETTINGS_MODULE=config.settings $(PYTHON) -m pytest

migrate:
\t$(MANAGE) migrate --noinput

collectstatic:
\t$(MANAGE) collectstatic --clear --noinput

runserver:
\t$(MANAGE) runserver 0.0.0.0:8000

shell:
\t$(MANAGE) shell
