#!/bin/bash
poetry run mypy src 2>&1 | tee .checks/mypy_output.txt