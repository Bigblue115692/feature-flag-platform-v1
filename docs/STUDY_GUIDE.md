# Study Guide

## Pass 1: understand the business purpose

Do not begin by memorizing syntax.

First be able to answer:

- What is a feature flag?
- Why would a team want a kill switch?
- Why use a percentage rollout?
- Why should the same user stay in the same cohort?
- What is the difference between an environment and a project?
- Why record audit history?

## Pass 2: follow one frontend action

Use the Disable button.

Find:

```text
FlagCard.jsx
api/client.js
views.py
serializers.py
services.py
repositories.py
models.py
```

Explain what each layer contributes.

## Pass 3: follow evaluation

Read `evaluation.py`.

Explain the difference between:

- global off
- premium targeting
- rule targeting
- percentage rollout

Then explain why hashing is used instead of randomness.

## Pass 4: database

Draw:

```text
Project -> Environment -> FeatureFlag -> TargetingRule
```

Explain the foreign keys.

Explain the unique constraints.

Explain what database indexes try to improve.

## Pass 5: infrastructure

Read:

```text
docker-compose.yml
backend/Dockerfile
frontend/Dockerfile
nginx/default.conf
config/settings.py
config/celery.py
```

Be able to explain why each process exists.

## Pass 6: tests

Read tests before changing code.

Try modifications:

- change rollout from 25% to 50%
- add a new rule operator
- add a user plan targeting rule
- add an endpoint that returns active flags for an environment

## Interview practice questions

1. What happens when you click Disable?
2. How does rollout percentage work?
3. Why not use random numbers?
4. Why is `enabled=False` checked before targeting rules?
5. Why is there a repository if Django already has an ORM?
6. What does the service layer own?
7. What is Redis doing here?
8. What does Celery do?
9. Why would evaluation audit records become expensive at scale?
10. What breaks first if traffic grows by 1000x?
