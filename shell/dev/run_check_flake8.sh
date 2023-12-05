#!/bin/bash
poetry run flake8 src 2>&1 | tee .checks/flake8_output.txt