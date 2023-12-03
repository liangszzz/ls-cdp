#!/bin/bash
poetry run flake8 --format=json --output-file=.checks/flake8_results.json src