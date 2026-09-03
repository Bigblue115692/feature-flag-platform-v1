#!/usr/bin/env sh
set -eu

docker compose down -v
docker compose up -d --build
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py seed_demo

echo "Development stack reset."
