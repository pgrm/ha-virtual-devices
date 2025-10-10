.PHONY: all setup format format-check lint test ci

all: setup format lint test

setup:
	poetry install --with dev
	poetry run lefthook install

format:
	poetry run ruff format .

format-check:
	poetry run ruff format --check .

lint:
	poetry run ruff check .

test:
	poetry run pytest --cov=custom_components.virtual_devices --cov-branch --cov-fail-under=90 tests/

json-check:
	find . -name "*.json" -print0 | xargs -0 -I {} python -m json.tool {} >/dev/null

ci: format-check lint test json-check
