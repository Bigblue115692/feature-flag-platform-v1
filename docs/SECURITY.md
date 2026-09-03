# Security Guide

## Current V1 posture

This repository is a study project.

The API permissions are intentionally open so local setup is frictionless.

That is not production-safe.

Before deploying publicly, authentication and authorization must be added.

## Authentication

Authentication answers:

> Who is making this request?

Possible approaches:

- session authentication for operator dashboard
- JWT or OAuth tokens
- service API keys for SDKs
- workload identity in cloud infrastructure

## Authorization

Authorization answers:

> Is this identity allowed to perform this action?

Potential roles:

```text
viewer
developer
operator
admin
```

Potential permissions:

```text
view flags
evaluate flags
create flags
modify rollout
disable flags
delete flags
view audit history
manage projects
```

A serious control plane should make destructive actions more restrictive than read-only actions.

## Tenant isolation

If multiple organizations share the platform, every query must be scoped to the tenant.

A missing tenant filter can become a cross-customer data exposure vulnerability.

Defense in depth can include:

- tenant foreign keys
- queryset scoping
- permission checks
- database row-level security
- tests that assert tenant isolation

## Input validation

DRF serializers validate request shapes.

Database constraints validate durable invariants.

Both matter.

Application validation improves error messages.

Database constraints remain authoritative under concurrency.

## Rate limiting

The evaluation endpoint can receive high traffic.

Rate limits protect capacity, but a production SDK path should be designed for much higher throughput than the operator API.

Administrative mutation endpoints should usually have stricter limits than runtime evaluation.

## CSRF

Session-authenticated browser mutations need CSRF protection.

Django includes CSRF middleware.

Token-authenticated APIs have different threat models.

## CORS

CORS controls which browser origins may read API responses.

CORS is not authentication.

A server-to-server caller is not constrained by browser CORS enforcement.

## Secrets

Never store plaintext production secrets in source control.

Rotate secrets if they are accidentally committed.

Use secret management systems and least-privilege credentials.

## Dependency security

Pin dependencies.

Run automated dependency scanning.

Patch frameworks and base images.

Remove packages that are no longer needed.

## Audit integrity

Audit records are security-relevant.

A more mature system might:

- make audit rows append-only
- prevent ordinary operators from deleting them
- export them to immutable storage
- cryptographically sign event chains

## HTTPS

Production traffic should use TLS.

Nginx in this local project listens on plain HTTP because it is designed for localhost development.
