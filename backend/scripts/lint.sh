#!/usr/bin/env bash
set -xeu

source .venv/bin/activate >/dev/null 2>&1

mypy portal
black portal
isort portal
flake8
autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place portal --exclude=__init__.py
