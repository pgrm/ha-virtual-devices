.PHONY: all setup format format-check lint lint-check test ci json-check

all: setup format lint test

setup:
	poetry install --with dev
	poetry run lefthook install

format:
	poetry run ruff format .

format-check:
	poetry run ruff format --check .

lint:
	poetry run ruff check --fix .

lint-check:
	poetry run ruff check .

test:
	poetry run pytest --cov=custom_components --cov-branch --cov-fail-under=90 --cov-report=term --cov-report=xml tests/

json-check:
	find . -name "*.json" -not -path "./.git/*" -not -path "./.venv/*" -exec python -m json.tool {} >/dev/null \;

ci: format-check lint-check test json-check
