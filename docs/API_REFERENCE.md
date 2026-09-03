# API Reference

## Projects

### List projects

```http
GET /api/v1/projects/
```

### Create project

```http
POST /api/v1/projects/
Content-Type: application/json

{
  "name": "Checkout Platform",
  "key": "checkout",
  "description": "Checkout experiments and delivery controls."
}
```

## Environments

### Create environment

```http
POST /api/v1/environments/
Content-Type: application/json

{
  "project": 1,
  "name": "Production",
  "key": "production"
}
```

## Feature flags

### Create flag

```http
POST /api/v1/flags/
Content-Type: application/json

{
  "environment": 1,
  "name": "New Checkout",
  "key": "new_checkout",
  "description": "Rewritten checkout experience",
  "enabled": true,
  "rollout_percentage": 10,
  "premium_only": false,
  "default_value": true,
  "off_value": false
}
```

### Update rollout

```http
PATCH /api/v1/flags/1/
Content-Type: application/json

{
  "rollout_percentage": 25
}
```

### Kill switch

```http
PATCH /api/v1/flags/1/
Content-Type: application/json

{
  "enabled": false
}
```

### Delete

```http
DELETE /api/v1/flags/1/
```

## Targeting

Create a rule attached to a flag:

```http
POST /api/v1/flags/1/targeting-rules/
Content-Type: application/json

{
  "priority": 10,
  "attribute": "country",
  "operator": "in",
  "comparison_value": ["US", "CA"],
  "enabled": true,
  "serve_value": true
}
```

Supported operators:

```text
equals
not_equals
in
not_in
contains
```

## Evaluation

```http
POST /api/v1/evaluate/
Content-Type: application/json

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

Possible result:

```json
{
  "flag_key": "new_checkout",
  "enabled": true,
  "value": true,
  "reason": "TARGETING_RULE_MATCH",
  "bucket": null,
  "rollout_percentage": 25,
  "matched_rule": 1
}
```

## Audit events

```http
GET /api/v1/audit-events/
```

Audit records include:

- entity type
- entity identifier
- action
- actor
- request ID
- metadata
- timestamp

## Health

```http
GET /health/
```

This only indicates that the web application process can answer.

## Readiness

```http
GET /ready/
```

This checks database and cache dependencies.
