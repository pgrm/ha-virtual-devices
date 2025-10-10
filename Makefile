.PHONY: all setup format format-check lint test ci

all: setup format lint test

setup:
	poetry install
	poetry run lefthook install

format:
	poetry run ruff format .

format-check:
	poetry run ruff format --check .

lint:
	poetry run ruff check .

test:
	poetry run pytest --cov=custom_components.virtual_devices --cov-branch --cov-fail-under=90 tests/

ci: format-check lint test
