# Glossary

## API

An application programming interface; here, HTTP endpoints exposed by Django REST Framework.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **API** appears conceptually. Explain what would break or become harder if that concept were removed.

## Audit log

A historical record of important actions such as creating, updating, deleting, or evaluating a flag.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Audit log** appears conceptually. Explain what would break or become harder if that concept were removed.

## Background worker

A process that executes queued jobs outside interactive HTTP requests.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Background worker** appears conceptually. Explain what would break or become harder if that concept were removed.

## Bucket

A deterministic integer assigned to an identity for percentage rollout decisions.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Bucket** appears conceptually. Explain what would break or become harder if that concept were removed.

## CORS

Browser cross-origin access policy controlled by HTTP headers.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **CORS** appears conceptually. Explain what would break or become harder if that concept were removed.

## Cache

A faster temporary copy of data used to reduce repeated expensive reads.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Cache** appears conceptually. Explain what would break or become harder if that concept were removed.

## Cache invalidation

Removing or replacing cached data when the authoritative data changes.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Cache invalidation** appears conceptually. Explain what would break or become harder if that concept were removed.

## Celery

A Python distributed task queue used here for background jobs.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Celery** appears conceptually. Explain what would break or become harder if that concept were removed.

## Client

Software that sends requests to another service; a browser, React app, or SDK can be a client.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Client** appears conceptually. Explain what would break or become harder if that concept were removed.

## Cohort

A stable group of users selected by rollout logic.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Cohort** appears conceptually. Explain what would break or become harder if that concept were removed.

## Control plane

The administrative system where operators define feature configuration.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Control plane** appears conceptually. Explain what would break or become harder if that concept were removed.

## DRF

Django REST Framework, a toolkit for building HTTP APIs on Django.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **DRF** appears conceptually. Explain what would break or become harder if that concept were removed.

## Database index

A data structure that speeds selected queries while adding write and storage cost.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Database index** appears conceptually. Explain what would break or become harder if that concept were removed.

## Deterministic

Producing the same output for the same input.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Deterministic** appears conceptually. Explain what would break or become harder if that concept were removed.

## Django ORM

Django's object-relational mapper for querying and updating relational data using Python objects.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Django ORM** appears conceptually. Explain what would break or become harder if that concept were removed.

## Environment

A deployment context such as development, staging, or production.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Environment** appears conceptually. Explain what would break or become harder if that concept were removed.

## Evaluation

The act of deciding what value a feature flag serves for a specific context.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Evaluation** appears conceptually. Explain what would break or become harder if that concept were removed.

## Feature flag

Configuration that changes application behavior without requiring a new code deployment.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Feature flag** appears conceptually. Explain what would break or become harder if that concept were removed.

## Foreign key

A relational database reference from one row/table to another.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Foreign key** appears conceptually. Explain what would break or become harder if that concept were removed.

## Gunicorn

A production-oriented Python WSGI server used to run Django processes.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Gunicorn** appears conceptually. Explain what would break or become harder if that concept were removed.

## Hash

A deterministic transformation from input bytes to a fixed-size digest.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Hash** appears conceptually. Explain what would break or become harder if that concept were removed.

## Health check

An endpoint indicating that an application process is alive enough to respond.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Health check** appears conceptually. Explain what would break or become harder if that concept were removed.

## Idempotency

A property where repeating an operation does not produce unintended additional effects.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Idempotency** appears conceptually. Explain what would break or become harder if that concept were removed.

## Kill switch

A high-priority mechanism to disable a feature quickly.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Kill switch** appears conceptually. Explain what would break or become harder if that concept were removed.

## Latency

Elapsed time between initiating an operation and receiving its result.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Latency** appears conceptually. Explain what would break or become harder if that concept were removed.

## Middleware

Code that wraps request processing before and after a view.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Middleware** appears conceptually. Explain what would break or become harder if that concept were removed.

## Migration

A versioned database schema change managed by Django.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Migration** appears conceptually. Explain what would break or become harder if that concept were removed.

## Monolith

An application deployed as one main unit, even if internally organized into modules.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Monolith** appears conceptually. Explain what would break or become harder if that concept were removed.

## Multitenancy

Serving multiple organizations while keeping their data and permissions isolated.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Multitenancy** appears conceptually. Explain what would break or become harder if that concept were removed.

## Nginx

A reverse proxy and web server used here as the single HTTP entry point.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Nginx** appears conceptually. Explain what would break or become harder if that concept were removed.

## Percentage rollout

Serving a feature to a deterministic percentage of identities.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Percentage rollout** appears conceptually. Explain what would break or become harder if that concept were removed.

## PostgreSQL

The relational database used as the authoritative configuration store.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **PostgreSQL** appears conceptually. Explain what would break or become harder if that concept were removed.

## Project

A logical grouping containing environments and feature flags.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Project** appears conceptually. Explain what would break or become harder if that concept were removed.

## REST

An architectural style commonly used for resource-oriented HTTP APIs.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **REST** appears conceptually. Explain what would break or become harder if that concept were removed.

## Readiness check

An endpoint indicating whether an instance should currently receive traffic.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Readiness check** appears conceptually. Explain what would break or become harder if that concept were removed.

## Redis

An in-memory data store used for caching and as Celery infrastructure.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Redis** appears conceptually. Explain what would break or become harder if that concept were removed.

## Repository layer

A code layer that centralizes data-access queries and persistence operations.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Repository layer** appears conceptually. Explain what would break or become harder if that concept were removed.

## Request ID

A correlation identifier attached to a request for debugging across logs.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Request ID** appears conceptually. Explain what would break or become harder if that concept were removed.

## Retry

Repeating a failed operation, usually with limits and delay.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Retry** appears conceptually. Explain what would break or become harder if that concept were removed.

## Rollout

Gradually exposing a feature to more users.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Rollout** appears conceptually. Explain what would break or become harder if that concept were removed.

## Serializer

DRF component that validates incoming data and renders outgoing representations.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Serializer** appears conceptually. Explain what would break or become harder if that concept were removed.

## Service layer

A code layer that coordinates application use cases and business operations.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Service layer** appears conceptually. Explain what would break or become harder if that concept were removed.

## Stable hashing

Hash-based cohort selection that keeps an identity in the same rollout bucket.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Stable hashing** appears conceptually. Explain what would break or become harder if that concept were removed.

## TTL

Time to live; the duration before cached data expires.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **TTL** appears conceptually. Explain what would break or become harder if that concept were removed.

## Targeting rule

A condition that selects users by attributes such as plan or country.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Targeting rule** appears conceptually. Explain what would break or become harder if that concept were removed.

## Transaction

A database unit of work that commits all included changes together or rolls them back.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Transaction** appears conceptually. Explain what would break or become harder if that concept were removed.

## Unique constraint

A database rule preventing duplicate values within a defined scope.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Unique constraint** appears conceptually. Explain what would break or become harder if that concept were removed.

## Vite

Frontend development/build tool used by the React application.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Vite** appears conceptually. Explain what would break or become harder if that concept were removed.

## WSGI

The Python web-server interface used by traditional Django deployments.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **WSGI** appears conceptually. Explain what would break or become harder if that concept were removed.

## Web server

A process that accepts HTTP traffic.

### Why it matters here

When studying the feature flag platform, locate at least one file or request path where **Web server** appears conceptually. Explain what would break or become harder if that concept were removed.

