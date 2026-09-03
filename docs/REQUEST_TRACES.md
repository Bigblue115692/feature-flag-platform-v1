# Request Traces

## Disable a flag

```text
Operator clicks Disable
  |
  v
FlagCard.toggleEnabled()
  |
  v
api.updateFlag(id, { enabled: false })
  |
  v
fetch PATCH /api/v1/flags/:id/
  |
  v
Nginx
  |
  v
Django URL resolver
  |
  v
FeatureFlagViewSet
  |
  v
FeatureFlagSerializer
  |
  v
FeatureFlagService.update_flag()
  |
  +--> snapshot old state
  |
  +--> FeatureFlagRepository.update()
  |      |
  |      v
  |    Django ORM
  |      |
  |      v
  |   PostgreSQL UPDATE
  |
  +--> AuditService.record()
  |      |
  |      v
  |   PostgreSQL INSERT
  |
  +--> FlagCache.invalidate()
         |
         v
       Redis DELETE

HTTP 200 JSON response
  |
  v
React replaces the local flag object
```

## Evaluate a user

```text
Client POST /api/v1/evaluate/
  |
  v
EvaluationRequestSerializer
  |
  v
FeatureFlagService.evaluate()
  |
  +--> FeatureFlagRepository.get_for_evaluation()
  |      |
  |      +--> select_related project/environment
  |      +--> prefetch targeting rules
  |
  +--> EvaluationContext
  |
  +--> FeatureEvaluator.evaluate()
         |
         +--> global enabled check
         +--> premium gate
         +--> targeting rules select an eligible value or explicitly serve off
         +--> enabling rule matches continue to the stable rollout bucket

AuditService.record(evaluate)
  |
  v
EvaluationResponseSerializer
  |
  v
HTTP 200
```
