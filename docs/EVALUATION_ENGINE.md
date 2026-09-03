# Evaluation Engine Notes

## Goal

Given:

- project
- environment
- flag
- user identity
- user attributes

return a stable decision and a reason.

## Inputs

Example:

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

## Outputs

```json
{
  "flag_key": "new_checkout",
  "enabled": true,
  "value": true,
  "reason": "ROLLOUT_MATCH",
  "bucket": 1732,
  "rollout_percentage": 25,
  "matched_rule": 1
}
```

## Reasons

- `FLAG_DISABLED`
- `PREMIUM_REQUIRED`
- `TARGETING_RULE_MATCH`
- `ROLLOUT_ZERO`
- `ROLLOUT_FULL`
- `ROLLOUT_MATCH`
- `ROLLOUT_MISS`

Reasons matter because operators need to understand why a decision occurred.

Without reasons, debugging becomes guesswork.

## Targeting and rollout order

An enabling targeting rule does not bypass percentage rollout. It selects the
value the user is eligible to receive, and then the stable user bucket decides
whether that value is served. The response keeps `matched_rule` populated so
operators can see that both targeting and rollout participated in the decision.

A targeting rule whose `serve_value` is false is an explicit exclusion and
returns the off value immediately.

## Boolean flags vs multivariate flags

The model stores JSON values for `default_value` and `off_value`.

That means the database can eventually support more than booleans.

Examples:

```json
{"theme": "compact"}
```

or

```json
"variant-b"
```

V1's UI focuses on boolean behavior, but the backend shape is intentionally extensible.
