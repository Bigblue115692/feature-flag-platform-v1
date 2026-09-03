#!/usr/bin/env sh
set -eu
docker compose exec backend python manage.py shell
