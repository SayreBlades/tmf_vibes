.PHONY: check format lint typecheck test

UV_RUN = uv run

all: check

check: format lint typecheck test
	@echo "All checks passed."

format:
	@$(UV_RUN) ruff format . > /dev/null

lint:
	@echo "Running linter..."
	@$(UV_RUN) ruff check --fix .

typecheck:
	@echo "Running type checker..."
	@$(UV_RUN) mypy some_legacy_platform/src

test-some-legacy-platform:
	@echo "Running some-legacy-platform tests..."
	@cd some_legacy_platform && $(UV_RUN) pytest . --tb=short

test: test-some-legacy-platform

run-some-legacy-platform:
	@echo "Starting Some Legacy Platform mock server on http://127.0.0.1:8081 ..."
	# Point to the app within the src/some_legacy_platform package
	@cd some_legacy_platform && $(UV_RUN) uvicorn src.some_legacy_platform.main:app --reload --port 8081
