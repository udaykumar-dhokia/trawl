.PHONY: help install dev-install test lint format type-check clean build docs serve

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install trawl in production mode
	uv sync --no-dev

dev-install: ## Install trawl in development mode
	uv sync

test: ## Run test suite
	uv run pytest

test-cov: ## Run tests with coverage
	uv run pytest --cov=trawl --cov-report=html

lint: ## Run linting
	uv run ruff check .

format: ## Format code
	uv run ruff format .

type-check: ## Run type checking
	uv run mypy .

check: lint type-check test ## Run all checks

clean: ## Clean up build artifacts and cache
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: ## Build package
	uv build

docs: ## Generate documentation
	@echo "Documentation generation not yet implemented"

serve: ## Run the API server
	uv run trawl

tui: ## Run the TUI interface
	uv run trawl --tui

docker-build: ## Build Docker image
	docker build -t trawl .

docker-run: ## Run Docker container
	docker run -p 8000:8000 trawl

release: clean check build ## Prepare for release
	@echo "Ready for release!"