# Feature Flag Platform V1

A complete learning-oriented V1 of a feature management and progressive delivery platform.

## V1 capabilities

- FastAPI backend
- SQLAlchemy persistence
- SQLite by default
- Projects and environments
- Multiple feature flags
- Global enable/disable
- Premium-only targeting
- Percentage rollout
- Deterministic SHA-256 bucketing
- Attribute targeting rules
- SDK-style evaluation endpoint
- Admin and SDK API keys
- Audit log
- React + TypeScript dashboard
- Flag creation and editing
- Evaluation playground
- Seed/demo data
- Pytest tests
- Docker Compose
- Auto-generated OpenAPI docs

## Architecture

```text
React dashboard
      |
      v
FastAPI routes
      |
      v
Repository + evaluation layer
      |
      v
SQLAlchemy
      |
      v
Database
```

## Backend quick start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
Copy-Item .env.example .env
python -m backend.scripts.seed
python -m uvicorn backend.app.main:app --reload
```

Then open:

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/health

## Frontend quick start

```powershell
cd frontend
npm install
npm run dev
```

Then open:

- http://127.0.0.1:5173

## Development API keys

The default development keys are:

```text
Admin: dev-admin-key
SDK:   dev-sdk-key
```

## Core evaluation flow

1. Find project + environment + flag.
2. Reject if the flag is globally disabled.
3. Reject if premium-only is enabled and the user is not premium.
4. Evaluate targeting rules.
5. Hash project/environment/flag/user together.
6. Map the hash into one of 10,000 buckets.
7. Compare that bucket against the configured rollout percentage.
8. Return enabled/disabled plus a reason.

## Example evaluation request

```json
{
  "project_key": "demo",
  "environment_key": "production",
  "flag_key": "new_checkout",
  "user": {
    "id": "user-107",
    "premium": true,
    "attributes": {
      "country": "US"
    }
  }
}
```

## Run tests

```powershell
pytest backend/tests -q
```

## V2 ideas

- PostgreSQL + Alembic migrations
- Redis cache
- multi-tenant organizations
- RBAC
- streaming flag updates
- language SDKs
- metrics and tracing
- rate limiting
- webhooks
- experiments/analytics
