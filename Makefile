#!/usr/bin/env make

.PHONY: install crawl build serve

install:
	uv sync

crawl:
	uv run python crawl.py

build:
	uv run zensical build -f zensical.yml
	if [ -f fix_paths.py ]; then uv run python fix_paths.py; fi

serve:
	uv run zensical serve -f zensical.yml
