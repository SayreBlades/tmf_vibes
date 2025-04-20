.PHONY: check format lint typecheck test

UV_RUN = uv run

all: check

check: format lint typecheck test
	@echo "All checks passed."

format:
	@$(UV_RUN) ruff format . > /dev/null

lint:
	@echo "Running linter..."
	@$(UV_RUN) ruff check .

typecheck:
	@echo "Running type checker..."
	@$(UV_RUN) mypy src

test:
	@echo "Running tests..."
	@$(UV_RUN) pytest
