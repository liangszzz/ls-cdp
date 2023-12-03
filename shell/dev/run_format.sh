#!/bin/bash
poetry run isort src
poetry run black src
