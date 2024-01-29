#!/bin/sh

poetry run bandit -r src/main/cdp
poetry run flake8 src
poetry run mypy src