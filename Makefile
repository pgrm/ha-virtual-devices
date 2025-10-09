.PHONY: setup format format-check lint test ci

setup:
	poetry install

format:
	poetry run ruff format .

format-check:
	poetry run ruff format --check .

lint:
	poetry run ruff check .

test:
	poetry run pytest --cov=custom_components.virtual_devices --cov-branch --cov-fail-under=90 --cov-report=term --cov-report=xml tests/

ci: format-check lint test
