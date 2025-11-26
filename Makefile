.PHONY: help install-dev lint format test check docker-up docker-down

help:
	@echo "Common developer commands:"
	@echo "  make install-dev   Install dev requirements"
	@echo "  make lint          Run Ruff and Black in check mode"
	@echo "  make format        Format code with Black and Ruff"
	@echo "  make test          Run pytest with coverage"
	@echo "  make check         Run lint + tests (CI parity)"

install-dev:
	pip install -r requirements-dev.txt

lint:
	ruff check .
	black --check .

format:
	ruff check --fix .
	black .

test:
	pytest --cov=.

check: lint test

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down
