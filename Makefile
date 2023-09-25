.PHONY: lint format check-format type-check test mypy

all: lint format

install-lint:
	pip install flake8 black mypy isort

install-test:
	pip install tox

lint: check-format type-check
	@echo "Linting code with flake8..."
	flake8 src/archive/

format:
	@echo "Formatting code with isort..."
	isort src/archive/
	@echo "Formatting code with Black..."
	black src/archive/

check-format:
	@echo "Checking code format with Black..."
	isort src/archive/ --check --diff
	black --check --diff src/archive/

type-check:
	@echo "Type-checking with mypy..."
	mypy src/archive/

test:
	@echo "Starting tests..."
	pytest

