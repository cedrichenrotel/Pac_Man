SHELL := /bin/bash
UV := uv
FILE := src/__main__.py
CONFIG := ./config.json
VENV := .venv
.PHONY: install run debug clean lint lint-strict

install: $(VENV)

$(VENV): pyproject.toml uv.lock
	$(UV) sync
	touch $(VENV)

run: install
	@$(UV) run python -m src $(CONFIG) 2> >(grep -v "MESA: warning: Driver does not support" >&2)

debug: install
	$(UV) run python -m pdb -m src $(CONFIG)

clean:
	find . -name "__pycache__" -type d -prune -exec rm -rf {} +
	find . -name "*.pyc" -delete
	rm -rf .mypy_cache .pytest_cache .ruff_cache .uv_cache
	rm -rf dist build build_hooks *.egg-info

lint: install
	$(UV) run flake8 .
	$(UV) run mypy . --warn-return-any \
	--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs \
	--check-untyped-defs

lint-strict: install
	$(UV) run flake8 .
	$(UV) run mypy . --strict
