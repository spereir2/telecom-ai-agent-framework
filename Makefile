.PHONY: help install up down smoke eval lint fmt typecheck test ci clean

OLLAMA_MODEL ?= qwen2.5:7b

help:
	@echo "Targets:"
	@echo "  install    - install dev dependencies (pip)"
	@echo "  up         - start ollama via docker compose"
	@echo "  down       - stop ollama"
	@echo "  smoke      - run nl-order against canonical example"
	@echo "  eval       - run eval harness against current OLLAMA_MODEL=$(OLLAMA_MODEL)"
	@echo "  lint       - ruff check"
	@echo "  fmt        - ruff format"
	@echo "  typecheck  - mypy"
	@echo "  test       - pytest"
	@echo "  ci         - lint + typecheck + test"

install:
	pip install -e ".[dev]"
	pre-commit install

up:
	docker compose up -d
	@echo "Pulling model $(OLLAMA_MODEL) (first run only)..."
	docker compose exec -T ollama ollama pull $(OLLAMA_MODEL)

down:
	docker compose down

smoke:
	nl-order "I'd like to order 500Mbps FTTH for 12 Baker Street, London W1U 6TS, account holder Jane Doe, jane@example.com"

eval:
	python -m evals.runner --model $(OLLAMA_MODEL)

lint:
	ruff check .

fmt:
	ruff format .

typecheck:
	mypy

test:
	pytest

ci: lint typecheck test

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
