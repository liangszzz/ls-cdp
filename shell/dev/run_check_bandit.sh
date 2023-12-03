#!/bin/bash
poetry run bandit -r -f json -o .checks/bandit_results.json src