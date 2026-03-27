#!/usr/bin/env bash

# Sair se houver um erro
set -o errexit

uv sync --frozen && uv cache prune --ci

uv run python manage.py collectstatic --no-input

uv run python manage.py migrate