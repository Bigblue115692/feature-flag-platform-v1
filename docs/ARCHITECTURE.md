# Architecture Deep Dive

## 1. Request lifecycle

The system is easiest to understand by following a single request.

Imagine an operator changes a feature flag rollout from 10% to 25%.

The React dashboard calls:

```http
PATCH /api/v1/flags/42/
Content-Type: application/json

{
  "rollout_percentage": 25
}
```

Nginx receives the request first. It forwards `/api/` traffic to Django.

Django resolves the URL to `FeatureFlagViewSet`.

Django REST Framework parses JSON into Python data.

`FeatureFlagSerializer` validates the payload.

`FeatureFlagViewSet.perform_update()` calls `FeatureFlagService.update_flag()`.

The service creates a snapshot of the previous state, then calls the repository.

`FeatureFlagRepository.update()` changes model fields, increments `version`, and saves through Django ORM.

Django ORM translates the model save into SQL for PostgreSQL.

The service writes an audit event and invalidates cache.

The serializer renders the updated model into JSON.

DRF produces an HTTP response.

Nginx sends it back to React.

React replaces the flag in local component state.

That full flow is intentionally visible in the project.

## 2. Why a service layer exists

Django does not require a service layer.

You could write:

```python
flag.rollout_percentage = 25
flag.save()
```

inside a view.

This project instead centralizes use-case logic in services.

That matters once an update means more than "save one row."

For example updating a flag currently means:

- snapshot old state
- persist changes
- increment version
- create audit event
- invalidate cache

If those operations were duplicated across views, admin jobs, CLI commands, and future GraphQL endpoints, behavior could diverge.

A service function becomes the application-level definition of the use case.

## 3. Why a repository layer exists

Django ORM is already a data-access abstraction.

A repository is therefore optional.

Here it exists for study and separation.

The service says:

```python
FeatureFlagRepository.get_for_evaluation(...)
```

rather than knowing the exact `select_related`, `prefetch_related`, and query expression.

This makes it easier to reason about:

- application/use-case logic
- query/data-access logic

The repository should not contain business policy. It should contain data retrieval and persistence behavior.

## 4. Stable rollout hashing

Feature rollouts must be stable.

Suppose a 10% rollout used:

```python
random.random() < 0.10
```

A user could receive the feature on one request and lose it on the next.

That makes debugging and user experience terrible.

Instead we hash a stable identity:

```text
project_key:environment_key:flag_key:user_id
```

SHA-256 gives a deterministic digest.

Part of that digest is converted to an integer.

Modulo 10,000 creates a stable bucket:

```text
0..9999
```

A 10% rollout uses:

```text
bucket < 1000
```

A 25% rollout uses:

```text
bucket < 2500
```

A 100% rollout uses every bucket.

This design also provides monotonic rollout behavior: users inside 10% remain inside 25%.

## 5. Targeting precedence

Evaluation order in V1:

1. Global enabled/disabled state
2. Premium-only gate
3. Explicit targeting rules
4. Percentage rollout

This ordering is a product decision.

A different system might allow targeting rules to bypass the global off switch, but that would make the kill switch less absolute.

V1 treats `enabled=False` as a hard kill switch.

## 6. Database model

The main relational chain is:

```text
Project
  |
  +-- Environment
        |
        +-- FeatureFlag
              |
              +-- TargetingRule
```

Audit events are separate because they represent append-oriented historical records.

A production system may partition evaluation logs away from administrative audit logs because evaluation volume can be dramatically larger.

## 7. Cache strategy

V1 includes Redis integration and a small cache abstraction.

The current evaluator loads optimized ORM objects directly.

The cache class demonstrates where cached serialized flag configuration would live.

A more advanced V2 could:

- cache flag configuration by project/environment/key
- use versioned cache keys
- publish invalidation events
- separate configuration cache from evaluation results
- use local process cache in SDKs

## 8. Celery

Celery is included for background work that should not slow interactive HTTP requests.

V1 demonstrates:

- pruning old evaluation audit records
- cache warming hook

Future jobs could include:

- rollout schedules
- webhook delivery
- analytics aggregation
- configuration snapshots
- stale flag reports

## 9. Nginx

Nginx acts as the edge reverse proxy in the local Docker stack.

It routes:

```text
/api/*   -> Django
/admin/* -> Django
/health  -> Django
/ready   -> Django
/*       -> React Vite server
```

In a production deployment the frontend would usually be built into static assets rather than served by Vite's development server.

## 10. Deployment evolution

V1 uses Docker Compose because it exposes infrastructure concepts without requiring Kubernetes.

A production evolution could look like:

```text
CDN
 -> load balancer
 -> stateless Django API replicas
 -> managed PostgreSQL
 -> managed Redis
 -> Celery worker pool
 -> object storage / logging / metrics
```

Only after scale requires it would it be reasonable to split components into independent services.
