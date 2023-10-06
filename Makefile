.PHONY: lint format check-format type-check test mypy install-lint

all: lint format

install-lint:
	pip install flake8 black mypy isort

lint: check-format type-check
	@echo "Linting code with flake8..."
	flake8 src/filepack/

format:
	@echo "Formatting code with isort..."
	isort src/filepack/
	@echo "Formatting code with Black..."
	black src/filepack/

check-format:
	@echo "Checking code format with Black..."
	isort src/filepack/ --check --diff
	black --check --diff src/filepack/

type-check:
	@echo "Type-checking with mypy..."
	mypy src/filepack/

test:
	@echo "Starting tests..."
	pytest

