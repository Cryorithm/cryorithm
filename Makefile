.PHONY: all $(shell grep '^[^#[:space:]].*:' Makefile | sed 's/:.*//')

help:
	@echo "Usage: make <target>"
	@echo "  help                 Show this help message"
	@echo "  build                Build the package using Poetry"
	@echo "  check                Perform all checks (linting, testing, and poetry integrity)"
	@echo "  check-poetry         Run 'poetry check'"
	@echo "  install              Reinstall the project requirements"
	@echo "  install-poetry       Reinstall the Poetry dependencies in sync mode"
	@echo "  install-precommit    Run 'pre-commit {clean,install}'"
	@echo "  lint                 Run 'pre-commit run all files'"
	@echo "  run                  Run a custom script 'my-script' within the Poetry environment"
	@echo "  shell                Start a shell within the Poetry virtual environment"
	@echo "  show                 Show all packages installed via Poetry"
	@echo "  test                 Run pytest within the Poetry environment"
	@echo "  update               Run 'poetry update' to update dependencies"
	@echo "  update-poetry        Update Poetry to the latest version"
	@echo "  update-requirements  Update the requirements.txt file"

build:
	poetry build

check: lint test check-poetry

check-poetry:
	poetry check

install:
	poetry install

install-poetry:
	poetry self install --sync

install-precommit:
	pre-commit clean
	pre-commit install

lint:
	poetry run pre-commit run --all-files

run: install update
	poetry run cryorithm-sensor-stock-fundamentals

shell:
	poetry shell

show:
	poetry show

test:
	poetry run pytest

update:
	poetry update

update-poetry:
	poetry self update

update-requirements:
	poetry run python ./helpers/update_requirements.py
