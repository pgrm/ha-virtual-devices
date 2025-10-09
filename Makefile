.PHONY: setup format lint test ci

setup:
	poetry install

format:
	poetry run ruff format .

lint:
	poetry run ruff check .

test:
	poetry run pytest --cov=custom_components.virtual_devices tests/

ci: format lint test
