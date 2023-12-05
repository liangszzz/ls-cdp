#!/bin/bash
poetry run pytest -v --cov=src/main/cdp --cov-branch --cov-fail-under=100 --cov-report=xml:.checks/coverage.xml