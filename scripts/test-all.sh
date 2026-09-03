#!/usr/bin/env sh
set -eu

docker compose exec backend python manage.py test apps
docker compose exec frontend npm run test -- --run
