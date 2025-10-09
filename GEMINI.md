# Gemini Project Guide: ha-virtual-devices

This document is a guide for Gemini and other AI bots to be the best possible assistant for this project.

**Note:** This document should be kept up-to-date with our conversations as the project evolves. Please update this file if our goals or priorities change.

## Project Goal

The primary goal is to develop and maintain **ha-virtual-devices**, a Home Assistant custom integration that provides smart "virtual devices" to abstract away the complexity of non-standard hardware.

The initial MVP is the **Virtual Step-Dimmer**, which will expose a Shelly-controlled step-dimmer as a standard, dimmable `light` entity in Home Assistant.

### Key objectives:

- **Abstraction:** Hide complex hardware logic (like multi-press toggling and power monitoring) behind simple, standard Home Assistant entities.
- **UI-First Configuration:** All virtual devices must be configurable via the Home Assistant UI (Config Flow). No YAML configuration should be required for defining devices.
- **Testability:** The core logic for each virtual device must be robust and have 100% test coverage using `pytest`. Tests should be able to run independently of a live Home Assistant instance.
- **Ease of Use:** The integration should be simple to install (via HACS) and configure for the end-user.

## Tech Stack and Tools

- **Platform:** Home Assistant Custom Integration
- **Language:** Python 3.12
- **Distribution:** HACS (Home Assistant Community Store)
- **Dependency Management:** Poetry
- **Testing Framework:** `pytest`
- **Linting & Formatting:** `ruff`
- **Task Runner:** Makefile
- **CI/CD:** GitHub Actions

## Development Workflow

The core integration code is located in the `custom_components/virtual_devices/` directory. Tests will be located in a top-level `tests/` directory.

All development tasks should be run using the `Makefile` targets, which ensures consistency between local development and the CI environment.

- **`make setup`**: Sets up the development environment by installing all dependencies with Poetry.
- **`make format`**: Formats all code using `ruff format`.
- **`make lint`**: Lints all code using `ruff check`.
- **`make test`**: Runs the `pytest` test suite and checks for 100% code coverage.
- **`make ci`**: Runs all non-modifying CI checks (`format-check`, `lint-check`, `test`). This is the command used by the GitHub Actions workflow.

### Conventions

- **Test-Driven:** All new logic must be accompanied by unit tests. The goal is 100% test coverage for the core logic. **Do not suggest or generate implementation code without also generating the corresponding tests.**
- **Linting and Formatting:** All Python code must pass the checks run by `make ci`. This ensures code is formatted and free of linter errors before committing.
- **Code Quality:** Adhere to Home Assistant developer best practices for custom integrations.

## How you can help

- **Boilerplate Generation:** Help generate the initial files and structure for the custom integration and its components (config flow, platforms, entities).
- **Logic Implementation:** Help write the core Python logic for the state machines that control the virtual devices.
- **Test Generation:** For any new code we add, **you must generate comprehensive unit tests using `pytest` and `pytest-mock`**. All code contributions must be testable and fully tested.
- **Documentation:** Help write clear docstrings and update the `README.md`.
- **Refactoring:** Suggest improvements to make the code more efficient, readable, and maintainable.
