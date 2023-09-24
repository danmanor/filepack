
SRC := .

.PHONY: lint format check-format type-check

all: lint format

install-lint:
	pip install flake8 black mypy

lint: check-format type-check
	@echo "Linting code with flake8..."
	flake8 $(SRC)

format:
	@echo "Formatting code with Black..."
	black $(SRC)

check-format:
	@echo "Checking code format with Black..."
	black --check $(SRC)

type-check:
	@echo "Type-checking with mypy..."
	mypy $(SRC)


