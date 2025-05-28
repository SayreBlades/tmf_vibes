.PHONY: check format format-core lint lint-core typecheck typecheck-core test run-core init-core

UV_RUN = uv run

LEGACY_DIR=some_legacy_platform
CORE_DIR=core_platform

all: check

check: format lint typecheck test
	@echo "All checks passed."

format: format-legacy format-core

format-legacy:
	@echo "Formatting legacy platform..."
	@cd $(LEGACY_DIR) && $(UV_RUN) ruff format .

format-core:
	@echo "Formatting core platform..."
	@cd $(CORE_DIR) && $(UV_RUN) ruff format .

lint: lint-legacy lint-core

lint-legacy:
	@echo "Linting legacy platform..."
	@cd $(LEGACY_DIR) && $(UV_RUN) ruff check --fix .

lint-core:
	@echo "Linting core platform..."
	@cd $(CORE_DIR) && $(UV_RUN) ruff check --fix .

typecheck: typecheck-legacy typecheck-core

typecheck-legacy:
	@echo "Type checking legacy platform..."
	@cd $(LEGACY_DIR) && $(UV_RUN) mypy src

typecheck-core:
	@echo "Type checking core platform..."
	@cd $(CORE_DIR) && $(UV_RUN) mypy src

test: test-legacy test-core

test-legacy:
	@echo "Running legacy platform tests..."
	@cd $(LEGACY_DIR) && $(UV_RUN) pytest . --tb=short

test-core:
	@echo "Running core platform tests..."
	@cd $(CORE_DIR) && $(UV_RUN) pytest . --tb=short

run-legacy:
	@echo "Starting Legacy Platform mock server on http://127.0.0.1:8081 ..."
	@cd $(LEGACY_DIR) && $(UV_RUN) uvicorn src.some_legacy_platform.main:app --reload --port 8081

run-core:
	@echo "Starting Core Platform on http://127.0.0.1:8000 ..."
	@cd $(CORE_DIR) && $(UV_RUN) uvicorn src.core_platform.main:app --reload --port 8000

init-core:
	@echo "Installing core platform dependencies..."
	@cd $(CORE_DIR) && $(UV_RUN) pip install -e .[dev]
