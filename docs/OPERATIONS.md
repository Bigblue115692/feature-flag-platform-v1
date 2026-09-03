# Operations Guide

## Purpose

This document explains how to reason about running the system rather than only writing code.

## Processes

The Docker Compose stack contains six process groups:

```text
db
redis
backend
worker
frontend
nginx
```

Each one has a separate responsibility.

### PostgreSQL

PostgreSQL is durable state.

If the backend process dies, flag configuration remains because PostgreSQL stores it on disk through a Docker volume.

The database should be treated as authoritative for:

- projects
- environments
- feature flags
- targeting rules
- audit events

### Redis

Redis is ephemeral infrastructure.

V1 uses it for:

- Django cache backend
- Celery broker
- Celery result backend

A more advanced architecture might separate those workloads into different Redis instances or use a dedicated message broker.

### Backend

The backend container runs Gunicorn.

Gunicorn starts multiple worker processes.

Each worker loads the Django application and can independently process HTTP requests.

This means in-memory Python state is not shared between workers.

That is one reason shared cache and durable state should live outside the process.

### Worker

The Celery worker imports Django settings and task definitions.

It waits for messages from Redis.

HTTP requests do not need to wait for background work to complete.

### Frontend

The V1 container runs Vite's development server.

This is deliberately convenient for study.

A production image would usually run:

```text
npm ci
npm run build
```

and copy the `dist` directory into Nginx or object storage.

### Nginx

Nginx exposes port 80.

The browser only needs to know one origin.

Nginx decides whether a request belongs to the frontend or backend.

## Failure scenarios

### PostgreSQL unavailable

Readiness should fail because the application cannot reliably read or update authoritative configuration.

The process may still be alive, so health can remain 200 while readiness becomes 503.

This distinction allows an orchestrator or load balancer to stop routing traffic without immediately restarting the process.

### Redis unavailable

Readiness currently fails.

A production platform could choose a degraded mode where direct database evaluation continues while cache and background jobs are unavailable.

That becomes a product and reliability decision.

### One backend worker crashes

Gunicorn can keep serving through other workers.

The crashed worker can be restarted.

Because state is externalized, another worker can continue from the same database.

### Frontend unavailable

SDK evaluation through the backend can continue.

The operator dashboard is unavailable, but runtime feature delivery can still work.

That separation is valuable.

## Backups

Important backup target:

```text
PostgreSQL
```

Redis should not need to be backed up for correctness in this V1.

Possible backup strategy:

- managed database snapshots
- point-in-time recovery
- periodic restore tests

A backup that has never been restored is only an assumption.

## Secrets

Do not commit `.env`.

Production secrets should live in a secret manager.

Examples:

- Django secret key
- database password
- API authentication secrets
- webhook signing secrets

## Logs

V1 emits application logs to stdout.

Containers and cloud platforms can collect stdout.

Useful future fields:

- timestamp
- severity
- request_id
- route
- status_code
- latency
- project_key
- environment_key
- flag_key

Avoid logging sensitive user attributes unless required and governed.

## Metrics

A production V2 should measure at minimum:

- request count
- request latency
- error rate
- evaluation count
- evaluation latency
- database query time
- Redis latency
- Celery queue depth
- worker failures
- percentage of cache hits

Metrics answer aggregate questions that logs do not answer efficiently.

## Tracing

Distributed tracing becomes more useful when one request crosses multiple services.

V1 is mostly a modular monolith, so request IDs provide much of the immediate debugging value.

If evaluation later spans API, configuration service, event bus, and analytics service, tracing becomes far more valuable.

## Deployments

A safe deployment sequence:

1. build immutable image
2. run automated tests
3. run migrations
4. deploy new backend replicas
5. pass readiness checks
6. shift traffic
7. monitor error and latency metrics

Backward-compatible migrations are important during rolling deployments because old and new application versions may temporarily run against the same database.

## Capacity thinking

Suppose evaluation traffic grows.

First inspect:

- request latency
- CPU saturation
- database QPS
- repeated configuration reads
- audit write volume

Likely V1 bottlenecks:

1. writing one audit event for every evaluation
2. remote HTTP evaluation instead of local SDK evaluation
3. repeated database reads for configuration
4. single PostgreSQL write path

A realistic scaling evolution would reduce synchronous evaluation writes, aggressively cache configuration, and eventually let SDKs evaluate locally.
