#!/bin/bash
poetry run mypy src > .checks/mypy_output.txt 2>&1