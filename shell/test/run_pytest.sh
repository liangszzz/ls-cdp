#!/bin/bash
poetry run pytest -v --cov=src/main/cdp --cov-branch --cov-fail-under=100