# Feature Flag Platform V1

A production-flavored full-stack feature management platform built for study.

## Stack

- Frontend: React + Vite + JavaScript
- Backend: Python + Django + Django REST Framework
- Database: PostgreSQL
- Cache: Redis
- Background jobs: Celery
- Reverse proxy: Nginx
- Containers: Docker + Docker Compose
- CI: GitHub Actions
- Testing: pytest / Django test framework + Vitest

## Core capabilities

- Projects and environments
- Feature flag CRUD
- Kill switch / enable-disable
- Deterministic percentage rollout
- Premium-only targeting
- Attribute targeting rules
- Stable user bucketing
- Audit logging
- Evaluation endpoint
- Cache invalidation
- Rate limiting hooks
- Health/readiness endpoints
- Service + repository architecture
- React admin dashboard
- API client abstraction
- Dockerized local stack
- Seed data
- Backend and frontend tests

## Architecture

```text
Browser / React
      |
      v
Nginx reverse proxy
      |
      v
Django REST Framework
      |
      +--> Serializers / validation
      |
      +--> Service layer
      |      |
      |      +--> Evaluation engine
      |      +--> Audit service
      |      +--> Cache service
      |
      +--> Repository layer
              |
              v
          Django ORM
              |
              v
          PostgreSQL

Redis <---- cache / rate-limit data
Celery <--- background jobs
```

## Why this project is intentionally layered

A tiny Django project can place most logic inside views and model methods. This project intentionally separates responsibilities so you can trace a request through a more production-like architecture.

For example, disabling a flag follows this path:

```text
React button
  -> PATCH /api/v1/flags/:id/
  -> DRF viewset
  -> serializer validation
  -> FeatureFlagService.update_flag()
  -> FeatureFlagRepository.update()
  -> PostgreSQL
  -> AuditService.record()
  -> cache invalidation
  -> HTTP response
  -> React state refresh
```

## Percentage rollout

Rollout is deterministic. We never call random() to decide whether a request receives a feature.

Instead we hash:

```text
project_key:environment_key:flag_key:user_id
```

into a bucket from 0 to 9999.

A 25% rollout means buckets 0 through 2499 are enabled.

This means the same user stays in the same cohort until the rollout configuration changes.

## Quick start with Docker

1. Copy env file:

```bash
cp .env.example .env
```

2. Start services:

```bash
docker compose up --build
```

3. Run migrations:

```bash
docker compose exec backend python manage.py migrate
```

4. Seed example data:

```bash
docker compose exec backend python manage.py seed_demo
```

5. Open:

- Frontend: http://localhost
- Backend API: http://localhost/api/v1/
- Django admin: http://localhost/admin/
- Health: http://localhost/health/

## Local backend without Docker

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

## Local frontend

```bash
cd frontend
npm install
npm run dev
```

## Load testing

The repository includes a reproducible k6 evaluation test with a live dashboard
at `http://localhost:5665` and an exported HTML report. See
[`docs/LOAD_TESTING.md`](docs/LOAD_TESTING.md) for the smoke-test and five-minute
baseline commands.

Published results:

- [2026-09-03 V1 remote evaluation baseline](docs/benchmarks/2026-09-03-v1-baseline/README.md)
- [2026-09-04 V1 maximum-throughput ramp](docs/benchmarks/2026-09-04-throughput-ramp/README.md)
- [2026-09-04 V1 no-audit comparison](docs/benchmarks/2026-09-04-no-audit-comparison/README.md)

## Important endpoints

```text
GET    /api/v1/projects/
POST   /api/v1/projects/

GET    /api/v1/environments/
POST   /api/v1/environments/

GET    /api/v1/flags/
POST   /api/v1/flags/
GET    /api/v1/flags/:id/
PATCH  /api/v1/flags/:id/
DELETE /api/v1/flags/:id/

POST   /api/v1/evaluate/
GET    /api/v1/audit-events/

GET    /health/
GET    /ready/
```

## Example evaluation request

```json
{
  "project_key": "checkout",
  "environment_key": "production",
  "flag_key": "new_checkout",
  "user": {
    "id": "user-107",
    "premium": true,
    "country": "US",
    "plan": "pro"
  }
}
```

Example response:

```json
{
  "flag_key": "new_checkout",
  "enabled": true,
  "reason": "ROLLOUT_MATCH",
  "bucket": 1732,
  "rollout_percentage": 25,
  "matched_rule": null
}
```

## Study order

A useful top-down study sequence:

1. `frontend/src/pages/FlagsPage.jsx`
2. `frontend/src/api/client.js`
3. `backend/apps/flags/views.py`
4. `backend/apps/flags/serializers.py`
5. `backend/apps/flags/services.py`
6. `backend/apps/flags/evaluation.py`
7. `backend/apps/flags/repositories.py`
8. `backend/apps/flags/models.py`
9. `backend/config/settings.py`
10. `docker-compose.yml`
11. `nginx/default.conf`

## Notes

This is V1, not a claim that every production feature flag vendor uses exactly this architecture. It is intentionally designed to expose common full-stack and backend concepts in one coherent project.
