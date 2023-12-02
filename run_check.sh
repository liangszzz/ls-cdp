#!/bin/bash

poetry run flake8 src
poetry run mypy src