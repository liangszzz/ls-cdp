#!/bin/bash

poetry run mypy --json-report src > .checks/mypy_results.json