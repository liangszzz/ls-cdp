#!/bin/bash

poetry run flake8 src --count --exit-zero
poetry run mypy src