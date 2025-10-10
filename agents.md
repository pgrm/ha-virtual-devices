# Agent Instructions for ha-virtual-devices

This document provides instructions for AI agents like Jules on how to set up and work with this repository.

## Environment Setup

This project requires Python 3.13. The following script must be executed to prepare the environment before installing dependencies.

```bash
# Install Python 3.13.2 using the preinstalled pyenv
pyenv install 3.13.2

# Set the local Python version for this project directory
pyenv local 3.13.2

# Tell Poetry to use the newly installed Python version
poetry env use python3.13

# Install dependencies using the Makefile target
make setup
```

## Workflow

After the environment is set up, use the `Makefile` for all common tasks:

- `make format`: Format the code.
- `make lint`: Run linter checks.
- `make test`: Run the test suite.
- `make ci`: Run all CI checks.
