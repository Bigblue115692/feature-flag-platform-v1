# Feature Flag Platform Reference Guide

## Study chapter 1
### HTTP fundamentals
- A browser or SDK is an HTTP client. Django is an HTTP server application behind a WSGI server.
- GET should retrieve representations. POST commonly creates resources or invokes commands. PATCH partially updates a resource. DELETE removes a resource.
- Status codes communicate categories of outcomes. 2xx means success, 4xx means the caller should change something, and 5xx means the server failed.
- JSON is a serialization format, not the database itself. DRF parses JSON request bodies into Python primitives and serializes Python data back to JSON.
- Headers carry metadata such as content type, authentication, correlation identifiers, caching directives, and tracing information.

### Django request processing
- The WSGI application receives a request from Gunicorn and Django middleware begins processing.
- URL routing resolves the incoming path to a view.
- DRF viewsets provide reusable request dispatch for REST resources.
- Serializers validate incoming primitive data and convert model objects to outgoing representations.
- Services coordinate business use cases while repositories isolate query details.

### Database fundamentals
- PostgreSQL persists relational rows and enforces constraints that application code alone cannot safely guarantee under concurrency.
- A foreign key connects one table to another. Here environments belong to projects and flags belong to environments.
- A unique constraint prevents duplicate keys within a defined scope.
- Indexes speed up selected reads at the cost of extra storage and write overhead.
- Transactions let a group of database changes commit or roll back together.

### Caching
- Redis stores data in memory and can answer repeated lookups much faster than a relational query.
- Caches introduce staleness risk, so invalidation strategy matters.
- A cache key must encode the identity of the configuration it represents.
- Versioned or namespaced keys reduce accidental collisions.
- A cache should be treated as disposable; PostgreSQL remains the authoritative source in this project.

### Background jobs
- Celery workers run tasks outside the interactive HTTP request.
- Background processing is useful for expensive or retryable work such as webhook delivery and analytics aggregation.
- A broker such as Redis carries task messages from producers to workers.
- Tasks should be designed for retries because distributed systems can deliver work more than once.
- Idempotent task design reduces damage from duplicate execution.

### Frontend state
- React renders UI from component state and props.
- An event handler reacts to a click and usually calls an API abstraction.
- The API client translates a JavaScript object into a JSON request.
- After the server responds, state updates cause React to render a new UI.
- Keeping network code outside presentation components reduces repetition.

### Rollout systems
- Percentage rollout is cohort selection, not request-level randomness.
- Stable hashing means a user can repeatedly receive the same decision.
- Increasing rollout percentage should ideally include the cohort that already had the feature.
- A kill switch must be able to override normal rollout logic quickly.
- Targeting rules should produce explainable decisions so debugging is possible.

### Operational concerns
- Health endpoints answer whether the process is alive; readiness endpoints answer whether dependencies are usable.
- Request IDs help correlate logs from the same request.
- Rate limiting protects expensive endpoints from accidental or abusive traffic.
- Audit logs provide accountability for configuration changes.
- Metrics and tracing would be natural next additions for production observability.

### Check yourself

Explain this chapter without looking at the code. Then trace one concrete request and identify where each concept appears in the repository.

## Study chapter 2
### HTTP fundamentals
- A browser or SDK is an HTTP client. Django is an HTTP server application behind a WSGI server.
- GET should retrieve representations. POST commonly creates resources or invokes commands. PATCH partially updates a resource. DELETE removes a resource.
- Status codes communicate categories of outcomes. 2xx means success, 4xx means the caller should change something, and 5xx means the server failed.
- JSON is a serialization format, not the database itself. DRF parses JSON request bodies into Python primitives and serializes Python data back to JSON.
- Headers carry metadata such as content type, authentication, correlation identifiers, caching directives, and tracing information.

### Django request processing
- The WSGI application receives a request from Gunicorn and Django middleware begins processing.
- URL routing resolves the incoming path to a view.
- DRF viewsets provide reusable request dispatch for REST resources.
- Serializers validate incoming primitive data and convert model objects to outgoing representations.
- Services coordinate business use cases while repositories isolate query details.

### Database fundamentals
- PostgreSQL persists relational rows and enforces constraints that application code alone cannot safely guarantee under concurrency.
- A foreign key connects one table to another. Here environments belong to projects and flags belong to environments.
- A unique constraint prevents duplicate keys within a defined scope.
- Indexes speed up selected reads at the cost of extra storage and write overhead.
- Transactions let a group of database changes commit or roll back together.

### Caching
- Redis stores data in memory and can answer repeated lookups much faster than a relational query.
- Caches introduce staleness risk, so invalidation strategy matters.
- A cache key must encode the identity of the configuration it represents.
- Versioned or namespaced keys reduce accidental collisions.
- A cache should be treated as disposable; PostgreSQL remains the authoritative source in this project.

### Background jobs
- Celery workers run tasks outside the interactive HTTP request.
- Background processing is useful for expensive or retryable work such as webhook delivery and analytics aggregation.
- A broker such as Redis carries task messages from producers to workers.
- Tasks should be designed for retries because distributed systems can deliver work more than once.
- Idempotent task design reduces damage from duplicate execution.

### Frontend state
- React renders UI from component state and props.
- An event handler reacts to a click and usually calls an API abstraction.
- The API client translates a JavaScript object into a JSON request.
- After the server responds, state updates cause React to render a new UI.
- Keeping network code outside presentation components reduces repetition.

### Rollout systems
- Percentage rollout is cohort selection, not request-level randomness.
- Stable hashing means a user can repeatedly receive the same decision.
- Increasing rollout percentage should ideally include the cohort that already had the feature.
- A kill switch must be able to override normal rollout logic quickly.
- Targeting rules should produce explainable decisions so debugging is possible.

### Operational concerns
- Health endpoints answer whether the process is alive; readiness endpoints answer whether dependencies are usable.
- Request IDs help correlate logs from the same request.
- Rate limiting protects expensive endpoints from accidental or abusive traffic.
- Audit logs provide accountability for configuration changes.
- Metrics and tracing would be natural next additions for production observability.

### Check yourself

Explain this chapter without looking at the code. Then trace one concrete request and identify where each concept appears in the repository.

## Study chapter 3
### HTTP fundamentals
- A browser or SDK is an HTTP client. Django is an HTTP server application behind a WSGI server.
- GET should retrieve representations. POST commonly creates resources or invokes commands. PATCH partially updates a resource. DELETE removes a resource.
- Status codes communicate categories of outcomes. 2xx means success, 4xx means the caller should change something, and 5xx means the server failed.
- JSON is a serialization format, not the database itself. DRF parses JSON request bodies into Python primitives and serializes Python data back to JSON.
- Headers carry metadata such as content type, authentication, correlation identifiers, caching directives, and tracing information.

### Django request processing
- The WSGI application receives a request from Gunicorn and Django middleware begins processing.
- URL routing resolves the incoming path to a view.
- DRF viewsets provide reusable request dispatch for REST resources.
- Serializers validate incoming primitive data and convert model objects to outgoing representations.
- Services coordinate business use cases while repositories isolate query details.

### Database fundamentals
- PostgreSQL persists relational rows and enforces constraints that application code alone cannot safely guarantee under concurrency.
- A foreign key connects one table to another. Here environments belong to projects and flags belong to environments.
- A unique constraint prevents duplicate keys within a defined scope.
- Indexes speed up selected reads at the cost of extra storage and write overhead.
- Transactions let a group of database changes commit or roll back together.

### Caching
- Redis stores data in memory and can answer repeated lookups much faster than a relational query.
- Caches introduce staleness risk, so invalidation strategy matters.
- A cache key must encode the identity of the configuration it represents.
- Versioned or namespaced keys reduce accidental collisions.
- A cache should be treated as disposable; PostgreSQL remains the authoritative source in this project.

### Background jobs
- Celery workers run tasks outside the interactive HTTP request.
- Background processing is useful for expensive or retryable work such as webhook delivery and analytics aggregation.
- A broker such as Redis carries task messages from producers to workers.
- Tasks should be designed for retries because distributed systems can deliver work more than once.
- Idempotent task design reduces damage from duplicate execution.

### Frontend state
- React renders UI from component state and props.
- An event handler reacts to a click and usually calls an API abstraction.
- The API client translates a JavaScript object into a JSON request.
- After the server responds, state updates cause React to render a new UI.
- Keeping network code outside presentation components reduces repetition.

### Rollout systems
- Percentage rollout is cohort selection, not request-level randomness.
- Stable hashing means a user can repeatedly receive the same decision.
- Increasing rollout percentage should ideally include the cohort that already had the feature.
- A kill switch must be able to override normal rollout logic quickly.
- Targeting rules should produce explainable decisions so debugging is possible.

### Operational concerns
- Health endpoints answer whether the process is alive; readiness endpoints answer whether dependencies are usable.
- Request IDs help correlate logs from the same request.
- Rate limiting protects expensive endpoints from accidental or abusive traffic.
- Audit logs provide accountability for configuration changes.
- Metrics and tracing would be natural next additions for production observability.

### Check yourself

Explain this chapter without looking at the code. Then trace one concrete request and identify where each concept appears in the repository.

## Study chapter 4
### HTTP fundamentals
- A browser or SDK is an HTTP client. Django is an HTTP server application behind a WSGI server.
- GET should retrieve representations. POST commonly creates resources or invokes commands. PATCH partially updates a resource. DELETE removes a resource.
- Status codes communicate categories of outcomes. 2xx means success, 4xx means the caller should change something, and 5xx means the server failed.
- JSON is a serialization format, not the database itself. DRF parses JSON request bodies into Python primitives and serializes Python data back to JSON.
- Headers carry metadata such as content type, authentication, correlation identifiers, caching directives, and tracing information.

### Django request processing
- The WSGI application receives a request from Gunicorn and Django middleware begins processing.
- URL routing resolves the incoming path to a view.
- DRF viewsets provide reusable request dispatch for REST resources.
- Serializers validate incoming primitive data and convert model objects to outgoing representations.
- Services coordinate business use cases while repositories isolate query details.

### Database fundamentals
- PostgreSQL persists relational rows and enforces constraints that application code alone cannot safely guarantee under concurrency.
- A foreign key connects one table to another. Here environments belong to projects and flags belong to environments.
- A unique constraint prevents duplicate keys within a defined scope.
- Indexes speed up selected reads at the cost of extra storage and write overhead.
- Transactions let a group of database changes commit or roll back together.

### Caching
- Redis stores data in memory and can answer repeated lookups much faster than a relational query.
- Caches introduce staleness risk, so invalidation strategy matters.
- A cache key must encode the identity of the configuration it represents.
- Versioned or namespaced keys reduce accidental collisions.
- A cache should be treated as disposable; PostgreSQL remains the authoritative source in this project.

### Background jobs
- Celery workers run tasks outside the interactive HTTP request.
- Background processing is useful for expensive or retryable work such as webhook delivery and analytics aggregation.
- A broker such as Redis carries task messages from producers to workers.
- Tasks should be designed for retries because distributed systems can deliver work more than once.
- Idempotent task design reduces damage from duplicate execution.

### Frontend state
- React renders UI from component state and props.
- An event handler reacts to a click and usually calls an API abstraction.
- The API client translates a JavaScript object into a JSON request.
- After the server responds, state updates cause React to render a new UI.
- Keeping network code outside presentation components reduces repetition.

### Rollout systems
- Percentage rollout is cohort selection, not request-level randomness.
- Stable hashing means a user can repeatedly receive the same decision.
- Increasing rollout percentage should ideally include the cohort that already had the feature.
- A kill switch must be able to override normal rollout logic quickly.
- Targeting rules should produce explainable decisions so debugging is possible.

### Operational concerns
- Health endpoints answer whether the process is alive; readiness endpoints answer whether dependencies are usable.
- Request IDs help correlate logs from the same request.
- Rate limiting protects expensive endpoints from accidental or abusive traffic.
- Audit logs provide accountability for configuration changes.
- Metrics and tracing would be natural next additions for production observability.

### Check yourself

Explain this chapter without looking at the code. Then trace one concrete request and identify where each concept appears in the repository.

## Study chapter 5
### HTTP fundamentals
- A browser or SDK is an HTTP client. Django is an HTTP server application behind a WSGI server.
- GET should retrieve representations. POST commonly creates resources or invokes commands. PATCH partially updates a resource. DELETE removes a resource.
- Status codes communicate categories of outcomes. 2xx means success, 4xx means the caller should change something, and 5xx means the server failed.
- JSON is a serialization format, not the database itself. DRF parses JSON request bodies into Python primitives and serializes Python data back to JSON.
- Headers carry metadata such as content type, authentication, correlation identifiers, caching directives, and tracing information.

### Django request processing
- The WSGI application receives a request from Gunicorn and Django middleware begins processing.
- URL routing resolves the incoming path to a view.
- DRF viewsets provide reusable request dispatch for REST resources.
- Serializers validate incoming primitive data and convert model objects to outgoing representations.
- Services coordinate business use cases while repositories isolate query details.

### Database fundamentals
- PostgreSQL persists relational rows and enforces constraints that application code alone cannot safely guarantee under concurrency.
- A foreign key connects one table to another. Here environments belong to projects and flags belong to environments.
- A unique constraint prevents duplicate keys within a defined scope.
- Indexes speed up selected reads at the cost of extra storage and write overhead.
- Transactions let a group of database changes commit or roll back together.

### Caching
- Redis stores data in memory and can answer repeated lookups much faster than a relational query.
- Caches introduce staleness risk, so invalidation strategy matters.
- A cache key must encode the identity of the configuration it represents.
- Versioned or namespaced keys reduce accidental collisions.
- A cache should be treated as disposable; PostgreSQL remains the authoritative source in this project.

### Background jobs
- Celery workers run tasks outside the interactive HTTP request.
- Background processing is useful for expensive or retryable work such as webhook delivery and analytics aggregation.
- A broker such as Redis carries task messages from producers to workers.
- Tasks should be designed for retries because distributed systems can deliver work more than once.
- Idempotent task design reduces damage from duplicate execution.

### Frontend state
- React renders UI from component state and props.
- An event handler reacts to a click and usually calls an API abstraction.
- The API client translates a JavaScript object into a JSON request.
- After the server responds, state updates cause React to render a new UI.
- Keeping network code outside presentation components reduces repetition.

### Rollout systems
- Percentage rollout is cohort selection, not request-level randomness.
- Stable hashing means a user can repeatedly receive the same decision.
- Increasing rollout percentage should ideally include the cohort that already had the feature.
- A kill switch must be able to override normal rollout logic quickly.
- Targeting rules should produce explainable decisions so debugging is possible.

### Operational concerns
- Health endpoints answer whether the process is alive; readiness endpoints answer whether dependencies are usable.
- Request IDs help correlate logs from the same request.
- Rate limiting protects expensive endpoints from accidental or abusive traffic.
- Audit logs provide accountability for configuration changes.
- Metrics and tracing would be natural next additions for production observability.

### Check yourself

Explain this chapter without looking at the code. Then trace one concrete request and identify where each concept appears in the repository.

## Study chapter 6
### HTTP fundamentals
- A browser or SDK is an HTTP client. Django is an HTTP server application behind a WSGI server.
- GET should retrieve representations. POST commonly creates resources or invokes commands. PATCH partially updates a resource. DELETE removes a resource.
- Status codes communicate categories of outcomes. 2xx means success, 4xx means the caller should change something, and 5xx means the server failed.
- JSON is a serialization format, not the database itself. DRF parses JSON request bodies into Python primitives and serializes Python data back to JSON.
- Headers carry metadata such as content type, authentication, correlation identifiers, caching directives, and tracing information.

### Django request processing
- The WSGI application receives a request from Gunicorn and Django middleware begins processing.
- URL routing resolves the incoming path to a view.
- DRF viewsets provide reusable request dispatch for REST resources.
- Serializers validate incoming primitive data and convert model objects to outgoing representations.
- Services coordinate business use cases while repositories isolate query details.

### Database fundamentals
- PostgreSQL persists relational rows and enforces constraints that application code alone cannot safely guarantee under concurrency.
- A foreign key connects one table to another. Here environments belong to projects and flags belong to environments.
- A unique constraint prevents duplicate keys within a defined scope.
- Indexes speed up selected reads at the cost of extra storage and write overhead.
- Transactions let a group of database changes commit or roll back together.

### Caching
- Redis stores data in memory and can answer repeated lookups much faster than a relational query.
- Caches introduce staleness risk, so invalidation strategy matters.
- A cache key must encode the identity of the configuration it represents.
- Versioned or namespaced keys reduce accidental collisions.
- A cache should be treated as disposable; PostgreSQL remains the authoritative source in this project.

### Background jobs
- Celery workers run tasks outside the interactive HTTP request.
- Background processing is useful for expensive or retryable work such as webhook delivery and analytics aggregation.
- A broker such as Redis carries task messages from producers to workers.
- Tasks should be designed for retries because distributed systems can deliver work more than once.
- Idempotent task design reduces damage from duplicate execution.

### Frontend state
- React renders UI from component state and props.
- An event handler reacts to a click and usually calls an API abstraction.
- The API client translates a JavaScript object into a JSON request.
- After the server responds, state updates cause React to render a new UI.
- Keeping network code outside presentation components reduces repetition.

### Rollout systems
- Percentage rollout is cohort selection, not request-level randomness.
- Stable hashing means a user can repeatedly receive the same decision.
- Increasing rollout percentage should ideally include the cohort that already had the feature.
- A kill switch must be able to override normal rollout logic quickly.
- Targeting rules should produce explainable decisions so debugging is possible.

### Operational concerns
- Health endpoints answer whether the process is alive; readiness endpoints answer whether dependencies are usable.
- Request IDs help correlate logs from the same request.
- Rate limiting protects expensive endpoints from accidental or abusive traffic.
- Audit logs provide accountability for configuration changes.
- Metrics and tracing would be natural next additions for production observability.

### Check yourself

Explain this chapter without looking at the code. Then trace one concrete request and identify where each concept appears in the repository.

## Study chapter 7
### HTTP fundamentals
- A browser or SDK is an HTTP client. Django is an HTTP server application behind a WSGI server.
- GET should retrieve representations. POST commonly creates resources or invokes commands. PATCH partially updates a resource. DELETE removes a resource.
- Status codes communicate categories of outcomes. 2xx means success, 4xx means the caller should change something, and 5xx means the server failed.
- JSON is a serialization format, not the database itself. DRF parses JSON request bodies into Python primitives and serializes Python data back to JSON.
- Headers carry metadata such as content type, authentication, correlation identifiers, caching directives, and tracing information.

### Django request processing
- The WSGI application receives a request from Gunicorn and Django middleware begins processing.
- URL routing resolves the incoming path to a view.
- DRF viewsets provide reusable request dispatch for REST resources.
- Serializers validate incoming primitive data and convert model objects to outgoing representations.
- Services coordinate business use cases while repositories isolate query details.

### Database fundamentals
- PostgreSQL persists relational rows and enforces constraints that application code alone cannot safely guarantee under concurrency.
- A foreign key connects one table to another. Here environments belong to projects and flags belong to environments.
- A unique constraint prevents duplicate keys within a defined scope.
- Indexes speed up selected reads at the cost of extra storage and write overhead.
- Transactions let a group of database changes commit or roll back together.

### Caching
- Redis stores data in memory and can answer repeated lookups much faster than a relational query.
- Caches introduce staleness risk, so invalidation strategy matters.
- A cache key must encode the identity of the configuration it represents.
- Versioned or namespaced keys reduce accidental collisions.
- A cache should be treated as disposable; PostgreSQL remains the authoritative source in this project.

### Background jobs
- Celery workers run tasks outside the interactive HTTP request.
- Background processing is useful for expensive or retryable work such as webhook delivery and analytics aggregation.
- A broker such as Redis carries task messages from producers to workers.
- Tasks should be designed for retries because distributed systems can deliver work more than once.
- Idempotent task design reduces damage from duplicate execution.

### Frontend state
- React renders UI from component state and props.
- An event handler reacts to a click and usually calls an API abstraction.
- The API client translates a JavaScript object into a JSON request.
- After the server responds, state updates cause React to render a new UI.
- Keeping network code outside presentation components reduces repetition.

### Rollout systems
- Percentage rollout is cohort selection, not request-level randomness.
- Stable hashing means a user can repeatedly receive the same decision.
- Increasing rollout percentage should ideally include the cohort that already had the feature.
- A kill switch must be able to override normal rollout logic quickly.
- Targeting rules should produce explainable decisions so debugging is possible.

### Operational concerns
- Health endpoints answer whether the process is alive; readiness endpoints answer whether dependencies are usable.
- Request IDs help correlate logs from the same request.
- Rate limiting protects expensive endpoints from accidental or abusive traffic.
- Audit logs provide accountability for configuration changes.
- Metrics and tracing would be natural next additions for production observability.

### Check yourself

Explain this chapter without looking at the code. Then trace one concrete request and identify where each concept appears in the repository.

## Study chapter 8
### HTTP fundamentals
- A browser or SDK is an HTTP client. Django is an HTTP server application behind a WSGI server.
- GET should retrieve representations. POST commonly creates resources or invokes commands. PATCH partially updates a resource. DELETE removes a resource.
- Status codes communicate categories of outcomes. 2xx means success, 4xx means the caller should change something, and 5xx means the server failed.
- JSON is a serialization format, not the database itself. DRF parses JSON request bodies into Python primitives and serializes Python data back to JSON.
- Headers carry metadata such as content type, authentication, correlation identifiers, caching directives, and tracing information.

### Django request processing
- The WSGI application receives a request from Gunicorn and Django middleware begins processing.
- URL routing resolves the incoming path to a view.
- DRF viewsets provide reusable request dispatch for REST resources.
- Serializers validate incoming primitive data and convert model objects to outgoing representations.
- Services coordinate business use cases while repositories isolate query details.

### Database fundamentals
- PostgreSQL persists relational rows and enforces constraints that application code alone cannot safely guarantee under concurrency.
- A foreign key connects one table to another. Here environments belong to projects and flags belong to environments.
- A unique constraint prevents duplicate keys within a defined scope.
- Indexes speed up selected reads at the cost of extra storage and write overhead.
- Transactions let a group of database changes commit or roll back together.

### Caching
- Redis stores data in memory and can answer repeated lookups much faster than a relational query.
- Caches introduce staleness risk, so invalidation strategy matters.
- A cache key must encode the identity of the configuration it represents.
- Versioned or namespaced keys reduce accidental collisions.
- A cache should be treated as disposable; PostgreSQL remains the authoritative source in this project.

### Background jobs
- Celery workers run tasks outside the interactive HTTP request.
- Background processing is useful for expensive or retryable work such as webhook delivery and analytics aggregation.
- A broker such as Redis carries task messages from producers to workers.
- Tasks should be designed for retries because distributed systems can deliver work more than once.
- Idempotent task design reduces damage from duplicate execution.

### Frontend state
- React renders UI from component state and props.
- An event handler reacts to a click and usually calls an API abstraction.
- The API client translates a JavaScript object into a JSON request.
- After the server responds, state updates cause React to render a new UI.
- Keeping network code outside presentation components reduces repetition.

### Rollout systems
- Percentage rollout is cohort selection, not request-level randomness.
- Stable hashing means a user can repeatedly receive the same decision.
- Increasing rollout percentage should ideally include the cohort that already had the feature.
- A kill switch must be able to override normal rollout logic quickly.
- Targeting rules should produce explainable decisions so debugging is possible.

### Operational concerns
- Health endpoints answer whether the process is alive; readiness endpoints answer whether dependencies are usable.
- Request IDs help correlate logs from the same request.
- Rate limiting protects expensive endpoints from accidental or abusive traffic.
- Audit logs provide accountability for configuration changes.
- Metrics and tracing would be natural next additions for production observability.

### Check yourself

Explain this chapter without looking at the code. Then trace one concrete request and identify where each concept appears in the repository.

## Study chapter 9
### HTTP fundamentals
- A browser or SDK is an HTTP client. Django is an HTTP server application behind a WSGI server.
- GET should retrieve representations. POST commonly creates resources or invokes commands. PATCH partially updates a resource. DELETE removes a resource.
- Status codes communicate categories of outcomes. 2xx means success, 4xx means the caller should change something, and 5xx means the server failed.
- JSON is a serialization format, not the database itself. DRF parses JSON request bodies into Python primitives and serializes Python data back to JSON.
- Headers carry metadata such as content type, authentication, correlation identifiers, caching directives, and tracing information.

### Django request processing
- The WSGI application receives a request from Gunicorn and Django middleware begins processing.
- URL routing resolves the incoming path to a view.
- DRF viewsets provide reusable request dispatch for REST resources.
- Serializers validate incoming primitive data and convert model objects to outgoing representations.
- Services coordinate business use cases while repositories isolate query details.

### Database fundamentals
- PostgreSQL persists relational rows and enforces constraints that application code alone cannot safely guarantee under concurrency.
- A foreign key connects one table to another. Here environments belong to projects and flags belong to environments.
- A unique constraint prevents duplicate keys within a defined scope.
- Indexes speed up selected reads at the cost of extra storage and write overhead.
- Transactions let a group of database changes commit or roll back together.

### Caching
- Redis stores data in memory and can answer repeated lookups much faster than a relational query.
- Caches introduce staleness risk, so invalidation strategy matters.
- A cache key must encode the identity of the configuration it represents.
- Versioned or namespaced keys reduce accidental collisions.
- A cache should be treated as disposable; PostgreSQL remains the authoritative source in this project.

### Background jobs
- Celery workers run tasks outside the interactive HTTP request.
- Background processing is useful for expensive or retryable work such as webhook delivery and analytics aggregation.
- A broker such as Redis carries task messages from producers to workers.
- Tasks should be designed for retries because distributed systems can deliver work more than once.
- Idempotent task design reduces damage from duplicate execution.

### Frontend state
- React renders UI from component state and props.
- An event handler reacts to a click and usually calls an API abstraction.
- The API client translates a JavaScript object into a JSON request.
- After the server responds, state updates cause React to render a new UI.
- Keeping network code outside presentation components reduces repetition.

### Rollout systems
- Percentage rollout is cohort selection, not request-level randomness.
- Stable hashing means a user can repeatedly receive the same decision.
- Increasing rollout percentage should ideally include the cohort that already had the feature.
- A kill switch must be able to override normal rollout logic quickly.
- Targeting rules should produce explainable decisions so debugging is possible.

### Operational concerns
- Health endpoints answer whether the process is alive; readiness endpoints answer whether dependencies are usable.
- Request IDs help correlate logs from the same request.
- Rate limiting protects expensive endpoints from accidental or abusive traffic.
- Audit logs provide accountability for configuration changes.
- Metrics and tracing would be natural next additions for production observability.

### Check yourself

Explain this chapter without looking at the code. Then trace one concrete request and identify where each concept appears in the repository.

## Study chapter 10
### HTTP fundamentals
- A browser or SDK is an HTTP client. Django is an HTTP server application behind a WSGI server.
- GET should retrieve representations. POST commonly creates resources or invokes commands. PATCH partially updates a resource. DELETE removes a resource.
- Status codes communicate categories of outcomes. 2xx means success, 4xx means the caller should change something, and 5xx means the server failed.
- JSON is a serialization format, not the database itself. DRF parses JSON request bodies into Python primitives and serializes Python data back to JSON.
- Headers carry metadata such as content type, authentication, correlation identifiers, caching directives, and tracing information.

### Django request processing
- The WSGI application receives a request from Gunicorn and Django middleware begins processing.
- URL routing resolves the incoming path to a view.
- DRF viewsets provide reusable request dispatch for REST resources.
- Serializers validate incoming primitive data and convert model objects to outgoing representations.
- Services coordinate business use cases while repositories isolate query details.

### Database fundamentals
- PostgreSQL persists relational rows and enforces constraints that application code alone cannot safely guarantee under concurrency.
- A foreign key connects one table to another. Here environments belong to projects and flags belong to environments.
- A unique constraint prevents duplicate keys within a defined scope.
- Indexes speed up selected reads at the cost of extra storage and write overhead.
- Transactions let a group of database changes commit or roll back together.

### Caching
- Redis stores data in memory and can answer repeated lookups much faster than a relational query.
- Caches introduce staleness risk, so invalidation strategy matters.
- A cache key must encode the identity of the configuration it represents.
- Versioned or namespaced keys reduce accidental collisions.
- A cache should be treated as disposable; PostgreSQL remains the authoritative source in this project.

### Background jobs
- Celery workers run tasks outside the interactive HTTP request.
- Background processing is useful for expensive or retryable work such as webhook delivery and analytics aggregation.
- A broker such as Redis carries task messages from producers to workers.
- Tasks should be designed for retries because distributed systems can deliver work more than once.
- Idempotent task design reduces damage from duplicate execution.

### Frontend state
- React renders UI from component state and props.
- An event handler reacts to a click and usually calls an API abstraction.
- The API client translates a JavaScript object into a JSON request.
- After the server responds, state updates cause React to render a new UI.
- Keeping network code outside presentation components reduces repetition.

### Rollout systems
- Percentage rollout is cohort selection, not request-level randomness.
- Stable hashing means a user can repeatedly receive the same decision.
- Increasing rollout percentage should ideally include the cohort that already had the feature.
- A kill switch must be able to override normal rollout logic quickly.
- Targeting rules should produce explainable decisions so debugging is possible.

### Operational concerns
- Health endpoints answer whether the process is alive; readiness endpoints answer whether dependencies are usable.
- Request IDs help correlate logs from the same request.
- Rate limiting protects expensive endpoints from accidental or abusive traffic.
- Audit logs provide accountability for configuration changes.
- Metrics and tracing would be natural next additions for production observability.

### Check yourself

Explain this chapter without looking at the code. Then trace one concrete request and identify where each concept appears in the repository.

## Study chapter 11
### HTTP fundamentals
- A browser or SDK is an HTTP client. Django is an HTTP server application behind a WSGI server.
- GET should retrieve representations. POST commonly creates resources or invokes commands. PATCH partially updates a resource. DELETE removes a resource.
- Status codes communicate categories of outcomes. 2xx means success, 4xx means the caller should change something, and 5xx means the server failed.
- JSON is a serialization format, not the database itself. DRF parses JSON request bodies into Python primitives and serializes Python data back to JSON.
- Headers carry metadata such as content type, authentication, correlation identifiers, caching directives, and tracing information.

### Django request processing
- The WSGI application receives a request from Gunicorn and Django middleware begins processing.
- URL routing resolves the incoming path to a view.
- DRF viewsets provide reusable request dispatch for REST resources.
- Serializers validate incoming primitive data and convert model objects to outgoing representations.
- Services coordinate business use cases while repositories isolate query details.

### Database fundamentals
- PostgreSQL persists relational rows and enforces constraints that application code alone cannot safely guarantee under concurrency.
- A foreign key connects one table to another. Here environments belong to projects and flags belong to environments.
- A unique constraint prevents duplicate keys within a defined scope.
- Indexes speed up selected reads at the cost of extra storage and write overhead.
- Transactions let a group of database changes commit or roll back together.

### Caching
- Redis stores data in memory and can answer repeated lookups much faster than a relational query.
- Caches introduce staleness risk, so invalidation strategy matters.
- A cache key must encode the identity of the configuration it represents.
- Versioned or namespaced keys reduce accidental collisions.
- A cache should be treated as disposable; PostgreSQL remains the authoritative source in this project.

### Background jobs
- Celery workers run tasks outside the interactive HTTP request.
- Background processing is useful for expensive or retryable work such as webhook delivery and analytics aggregation.
- A broker such as Redis carries task messages from producers to workers.
- Tasks should be designed for retries because distributed systems can deliver work more than once.
- Idempotent task design reduces damage from duplicate execution.

### Frontend state
- React renders UI from component state and props.
- An event handler reacts to a click and usually calls an API abstraction.
- The API client translates a JavaScript object into a JSON request.
- After the server responds, state updates cause React to render a new UI.
- Keeping network code outside presentation components reduces repetition.

### Rollout systems
- Percentage rollout is cohort selection, not request-level randomness.
- Stable hashing means a user can repeatedly receive the same decision.
- Increasing rollout percentage should ideally include the cohort that already had the feature.
- A kill switch must be able to override normal rollout logic quickly.
- Targeting rules should produce explainable decisions so debugging is possible.

### Operational concerns
- Health endpoints answer whether the process is alive; readiness endpoints answer whether dependencies are usable.
- Request IDs help correlate logs from the same request.
- Rate limiting protects expensive endpoints from accidental or abusive traffic.
- Audit logs provide accountability for configuration changes.
- Metrics and tracing would be natural next additions for production observability.

### Check yourself

Explain this chapter without looking at the code. Then trace one concrete request and identify where each concept appears in the repository.

## Study chapter 12
### HTTP fundamentals
- A browser or SDK is an HTTP client. Django is an HTTP server application behind a WSGI server.
- GET should retrieve representations. POST commonly creates resources or invokes commands. PATCH partially updates a resource. DELETE removes a resource.
- Status codes communicate categories of outcomes. 2xx means success, 4xx means the caller should change something, and 5xx means the server failed.
- JSON is a serialization format, not the database itself. DRF parses JSON request bodies into Python primitives and serializes Python data back to JSON.
- Headers carry metadata such as content type, authentication, correlation identifiers, caching directives, and tracing information.

### Django request processing
- The WSGI application receives a request from Gunicorn and Django middleware begins processing.
- URL routing resolves the incoming path to a view.
- DRF viewsets provide reusable request dispatch for REST resources.
- Serializers validate incoming primitive data and convert model objects to outgoing representations.
- Services coordinate business use cases while repositories isolate query details.

### Database fundamentals
- PostgreSQL persists relational rows and enforces constraints that application code alone cannot safely guarantee under concurrency.
- A foreign key connects one table to another. Here environments belong to projects and flags belong to environments.
- A unique constraint prevents duplicate keys within a defined scope.
- Indexes speed up selected reads at the cost of extra storage and write overhead.
- Transactions let a group of database changes commit or roll back together.

### Caching
- Redis stores data in memory and can answer repeated lookups much faster than a relational query.
- Caches introduce staleness risk, so invalidation strategy matters.
- A cache key must encode the identity of the configuration it represents.
- Versioned or namespaced keys reduce accidental collisions.
- A cache should be treated as disposable; PostgreSQL remains the authoritative source in this project.

### Background jobs
- Celery workers run tasks outside the interactive HTTP request.
- Background processing is useful for expensive or retryable work such as webhook delivery and analytics aggregation.
- A broker such as Redis carries task messages from producers to workers.
- Tasks should be designed for retries because distributed systems can deliver work more than once.
- Idempotent task design reduces damage from duplicate execution.

### Frontend state
- React renders UI from component state and props.
- An event handler reacts to a click and usually calls an API abstraction.
- The API client translates a JavaScript object into a JSON request.
- After the server responds, state updates cause React to render a new UI.
- Keeping network code outside presentation components reduces repetition.

### Rollout systems
- Percentage rollout is cohort selection, not request-level randomness.
- Stable hashing means a user can repeatedly receive the same decision.
- Increasing rollout percentage should ideally include the cohort that already had the feature.
- A kill switch must be able to override normal rollout logic quickly.
- Targeting rules should produce explainable decisions so debugging is possible.

### Operational concerns
- Health endpoints answer whether the process is alive; readiness endpoints answer whether dependencies are usable.
- Request IDs help correlate logs from the same request.
- Rate limiting protects expensive endpoints from accidental or abusive traffic.
- Audit logs provide accountability for configuration changes.
- Metrics and tracing would be natural next additions for production observability.

### Check yourself

Explain this chapter without looking at the code. Then trace one concrete request and identify where each concept appears in the repository.

## Study chapter 13
### HTTP fundamentals
- A browser or SDK is an HTTP client. Django is an HTTP server application behind a WSGI server.
- GET should retrieve representations. POST commonly creates resources or invokes commands. PATCH partially updates a resource. DELETE removes a resource.
- Status codes communicate categories of outcomes. 2xx means success, 4xx means the caller should change something, and 5xx means the server failed.
- JSON is a serialization format, not the database itself. DRF parses JSON request bodies into Python primitives and serializes Python data back to JSON.
- Headers carry metadata such as content type, authentication, correlation identifiers, caching directives, and tracing information.

### Django request processing
- The WSGI application receives a request from Gunicorn and Django middleware begins processing.
- URL routing resolves the incoming path to a view.
- DRF viewsets provide reusable request dispatch for REST resources.
- Serializers validate incoming primitive data and convert model objects to outgoing representations.
- Services coordinate business use cases while repositories isolate query details.

### Database fundamentals
- PostgreSQL persists relational rows and enforces constraints that application code alone cannot safely guarantee under concurrency.
- A foreign key connects one table to another. Here environments belong to projects and flags belong to environments.
- A unique constraint prevents duplicate keys within a defined scope.
- Indexes speed up selected reads at the cost of extra storage and write overhead.
- Transactions let a group of database changes commit or roll back together.

### Caching
- Redis stores data in memory and can answer repeated lookups much faster than a relational query.
- Caches introduce staleness risk, so invalidation strategy matters.
- A cache key must encode the identity of the configuration it represents.
- Versioned or namespaced keys reduce accidental collisions.
- A cache should be treated as disposable; PostgreSQL remains the authoritative source in this project.

### Background jobs
- Celery workers run tasks outside the interactive HTTP request.
- Background processing is useful for expensive or retryable work such as webhook delivery and analytics aggregation.
- A broker such as Redis carries task messages from producers to workers.
- Tasks should be designed for retries because distributed systems can deliver work more than once.
- Idempotent task design reduces damage from duplicate execution.

### Frontend state
- React renders UI from component state and props.
- An event handler reacts to a click and usually calls an API abstraction.
- The API client translates a JavaScript object into a JSON request.
- After the server responds, state updates cause React to render a new UI.
- Keeping network code outside presentation components reduces repetition.

### Rollout systems
- Percentage rollout is cohort selection, not request-level randomness.
- Stable hashing means a user can repeatedly receive the same decision.
- Increasing rollout percentage should ideally include the cohort that already had the feature.
- A kill switch must be able to override normal rollout logic quickly.
- Targeting rules should produce explainable decisions so debugging is possible.

### Operational concerns
- Health endpoints answer whether the process is alive; readiness endpoints answer whether dependencies are usable.
- Request IDs help correlate logs from the same request.
- Rate limiting protects expensive endpoints from accidental or abusive traffic.
- Audit logs provide accountability for configuration changes.
- Metrics and tracing would be natural next additions for production observability.

### Check yourself

Explain this chapter without looking at the code. Then trace one concrete request and identify where each concept appears in the repository.

## Study chapter 14
### HTTP fundamentals
- A browser or SDK is an HTTP client. Django is an HTTP server application behind a WSGI server.
- GET should retrieve representations. POST commonly creates resources or invokes commands. PATCH partially updates a resource. DELETE removes a resource.
- Status codes communicate categories of outcomes. 2xx means success, 4xx means the caller should change something, and 5xx means the server failed.
- JSON is a serialization format, not the database itself. DRF parses JSON request bodies into Python primitives and serializes Python data back to JSON.
- Headers carry metadata such as content type, authentication, correlation identifiers, caching directives, and tracing information.

### Django request processing
- The WSGI application receives a request from Gunicorn and Django middleware begins processing.
- URL routing resolves the incoming path to a view.
- DRF viewsets provide reusable request dispatch for REST resources.
- Serializers validate incoming primitive data and convert model objects to outgoing representations.
- Services coordinate business use cases while repositories isolate query details.

### Database fundamentals
- PostgreSQL persists relational rows and enforces constraints that application code alone cannot safely guarantee under concurrency.
- A foreign key connects one table to another. Here environments belong to projects and flags belong to environments.
- A unique constraint prevents duplicate keys within a defined scope.
- Indexes speed up selected reads at the cost of extra storage and write overhead.
- Transactions let a group of database changes commit or roll back together.

### Caching
- Redis stores data in memory and can answer repeated lookups much faster than a relational query.
- Caches introduce staleness risk, so invalidation strategy matters.
- A cache key must encode the identity of the configuration it represents.
- Versioned or namespaced keys reduce accidental collisions.
- A cache should be treated as disposable; PostgreSQL remains the authoritative source in this project.

### Background jobs
- Celery workers run tasks outside the interactive HTTP request.
- Background processing is useful for expensive or retryable work such as webhook delivery and analytics aggregation.
- A broker such as Redis carries task messages from producers to workers.
- Tasks should be designed for retries because distributed systems can deliver work more than once.
- Idempotent task design reduces damage from duplicate execution.

### Frontend state
- React renders UI from component state and props.
- An event handler reacts to a click and usually calls an API abstraction.
- The API client translates a JavaScript object into a JSON request.
- After the server responds, state updates cause React to render a new UI.
- Keeping network code outside presentation components reduces repetition.

### Rollout systems
- Percentage rollout is cohort selection, not request-level randomness.
- Stable hashing means a user can repeatedly receive the same decision.
- Increasing rollout percentage should ideally include the cohort that already had the feature.
- A kill switch must be able to override normal rollout logic quickly.
- Targeting rules should produce explainable decisions so debugging is possible.

### Operational concerns
- Health endpoints answer whether the process is alive; readiness endpoints answer whether dependencies are usable.
- Request IDs help correlate logs from the same request.
- Rate limiting protects expensive endpoints from accidental or abusive traffic.
- Audit logs provide accountability for configuration changes.
- Metrics and tracing would be natural next additions for production observability.

### Check yourself

Explain this chapter without looking at the code. Then trace one concrete request and identify where each concept appears in the repository.

## Study chapter 15
### HTTP fundamentals
- A browser or SDK is an HTTP client. Django is an HTTP server application behind a WSGI server.
- GET should retrieve representations. POST commonly creates resources or invokes commands. PATCH partially updates a resource. DELETE removes a resource.
- Status codes communicate categories of outcomes. 2xx means success, 4xx means the caller should change something, and 5xx means the server failed.
- JSON is a serialization format, not the database itself. DRF parses JSON request bodies into Python primitives and serializes Python data back to JSON.
- Headers carry metadata such as content type, authentication, correlation identifiers, caching directives, and tracing information.

### Django request processing
- The WSGI application receives a request from Gunicorn and Django middleware begins processing.
- URL routing resolves the incoming path to a view.
- DRF viewsets provide reusable request dispatch for REST resources.
- Serializers validate incoming primitive data and convert model objects to outgoing representations.
- Services coordinate business use cases while repositories isolate query details.

### Database fundamentals
- PostgreSQL persists relational rows and enforces constraints that application code alone cannot safely guarantee under concurrency.
- A foreign key connects one table to another. Here environments belong to projects and flags belong to environments.
- A unique constraint prevents duplicate keys within a defined scope.
- Indexes speed up selected reads at the cost of extra storage and write overhead.
- Transactions let a group of database changes commit or roll back together.

### Caching
- Redis stores data in memory and can answer repeated lookups much faster than a relational query.
- Caches introduce staleness risk, so invalidation strategy matters.
- A cache key must encode the identity of the configuration it represents.
- Versioned or namespaced keys reduce accidental collisions.
- A cache should be treated as disposable; PostgreSQL remains the authoritative source in this project.

### Background jobs
- Celery workers run tasks outside the interactive HTTP request.
- Background processing is useful for expensive or retryable work such as webhook delivery and analytics aggregation.
- A broker such as Redis carries task messages from producers to workers.
- Tasks should be designed for retries because distributed systems can deliver work more than once.
- Idempotent task design reduces damage from duplicate execution.

### Frontend state
- React renders UI from component state and props.
- An event handler reacts to a click and usually calls an API abstraction.
- The API client translates a JavaScript object into a JSON request.
- After the server responds, state updates cause React to render a new UI.
- Keeping network code outside presentation components reduces repetition.

### Rollout systems
- Percentage rollout is cohort selection, not request-level randomness.
- Stable hashing means a user can repeatedly receive the same decision.
- Increasing rollout percentage should ideally include the cohort that already had the feature.
- A kill switch must be able to override normal rollout logic quickly.
- Targeting rules should produce explainable decisions so debugging is possible.

### Operational concerns
- Health endpoints answer whether the process is alive; readiness endpoints answer whether dependencies are usable.
- Request IDs help correlate logs from the same request.
- Rate limiting protects expensive endpoints from accidental or abusive traffic.
- Audit logs provide accountability for configuration changes.
- Metrics and tracing would be natural next additions for production observability.

### Check yourself

Explain this chapter without looking at the code. Then trace one concrete request and identify where each concept appears in the repository.

## Study chapter 16
### HTTP fundamentals
- A browser or SDK is an HTTP client. Django is an HTTP server application behind a WSGI server.
- GET should retrieve representations. POST commonly creates resources or invokes commands. PATCH partially updates a resource. DELETE removes a resource.
- Status codes communicate categories of outcomes. 2xx means success, 4xx means the caller should change something, and 5xx means the server failed.
- JSON is a serialization format, not the database itself. DRF parses JSON request bodies into Python primitives and serializes Python data back to JSON.
- Headers carry metadata such as content type, authentication, correlation identifiers, caching directives, and tracing information.

### Django request processing
- The WSGI application receives a request from Gunicorn and Django middleware begins processing.
- URL routing resolves the incoming path to a view.
- DRF viewsets provide reusable request dispatch for REST resources.
- Serializers validate incoming primitive data and convert model objects to outgoing representations.
- Services coordinate business use cases while repositories isolate query details.

### Database fundamentals
- PostgreSQL persists relational rows and enforces constraints that application code alone cannot safely guarantee under concurrency.
- A foreign key connects one table to another. Here environments belong to projects and flags belong to environments.
- A unique constraint prevents duplicate keys within a defined scope.
- Indexes speed up selected reads at the cost of extra storage and write overhead.
- Transactions let a group of database changes commit or roll back together.

### Caching
- Redis stores data in memory and can answer repeated lookups much faster than a relational query.
- Caches introduce staleness risk, so invalidation strategy matters.
- A cache key must encode the identity of the configuration it represents.
- Versioned or namespaced keys reduce accidental collisions.
- A cache should be treated as disposable; PostgreSQL remains the authoritative source in this project.

### Background jobs
- Celery workers run tasks outside the interactive HTTP request.
- Background processing is useful for expensive or retryable work such as webhook delivery and analytics aggregation.
- A broker such as Redis carries task messages from producers to workers.
- Tasks should be designed for retries because distributed systems can deliver work more than once.
- Idempotent task design reduces damage from duplicate execution.

### Frontend state
- React renders UI from component state and props.
- An event handler reacts to a click and usually calls an API abstraction.
- The API client translates a JavaScript object into a JSON request.
- After the server responds, state updates cause React to render a new UI.
- Keeping network code outside presentation components reduces repetition.

### Rollout systems
- Percentage rollout is cohort selection, not request-level randomness.
- Stable hashing means a user can repeatedly receive the same decision.
- Increasing rollout percentage should ideally include the cohort that already had the feature.
- A kill switch must be able to override normal rollout logic quickly.
- Targeting rules should produce explainable decisions so debugging is possible.

### Operational concerns
- Health endpoints answer whether the process is alive; readiness endpoints answer whether dependencies are usable.
- Request IDs help correlate logs from the same request.
- Rate limiting protects expensive endpoints from accidental or abusive traffic.
- Audit logs provide accountability for configuration changes.
- Metrics and tracing would be natural next additions for production observability.

### Check yourself

Explain this chapter without looking at the code. Then trace one concrete request and identify where each concept appears in the repository.

## Study chapter 17
### HTTP fundamentals
- A browser or SDK is an HTTP client. Django is an HTTP server application behind a WSGI server.
- GET should retrieve representations. POST commonly creates resources or invokes commands. PATCH partially updates a resource. DELETE removes a resource.
- Status codes communicate categories of outcomes. 2xx means success, 4xx means the caller should change something, and 5xx means the server failed.
- JSON is a serialization format, not the database itself. DRF parses JSON request bodies into Python primitives and serializes Python data back to JSON.
- Headers carry metadata such as content type, authentication, correlation identifiers, caching directives, and tracing information.

### Django request processing
- The WSGI application receives a request from Gunicorn and Django middleware begins processing.
- URL routing resolves the incoming path to a view.
- DRF viewsets provide reusable request dispatch for REST resources.
- Serializers validate incoming primitive data and convert model objects to outgoing representations.
- Services coordinate business use cases while repositories isolate query details.

### Database fundamentals
- PostgreSQL persists relational rows and enforces constraints that application code alone cannot safely guarantee under concurrency.
- A foreign key connects one table to another. Here environments belong to projects and flags belong to environments.
- A unique constraint prevents duplicate keys within a defined scope.
- Indexes speed up selected reads at the cost of extra storage and write overhead.
- Transactions let a group of database changes commit or roll back together.

### Caching
- Redis stores data in memory and can answer repeated lookups much faster than a relational query.
- Caches introduce staleness risk, so invalidation strategy matters.
- A cache key must encode the identity of the configuration it represents.
- Versioned or namespaced keys reduce accidental collisions.
- A cache should be treated as disposable; PostgreSQL remains the authoritative source in this project.

### Background jobs
- Celery workers run tasks outside the interactive HTTP request.
- Background processing is useful for expensive or retryable work such as webhook delivery and analytics aggregation.
- A broker such as Redis carries task messages from producers to workers.
- Tasks should be designed for retries because distributed systems can deliver work more than once.
- Idempotent task design reduces damage from duplicate execution.

### Frontend state
- React renders UI from component state and props.
- An event handler reacts to a click and usually calls an API abstraction.
- The API client translates a JavaScript object into a JSON request.
- After the server responds, state updates cause React to render a new UI.
- Keeping network code outside presentation components reduces repetition.

### Rollout systems
- Percentage rollout is cohort selection, not request-level randomness.
- Stable hashing means a user can repeatedly receive the same decision.
- Increasing rollout percentage should ideally include the cohort that already had the feature.
- A kill switch must be able to override normal rollout logic quickly.
- Targeting rules should produce explainable decisions so debugging is possible.

### Operational concerns
- Health endpoints answer whether the process is alive; readiness endpoints answer whether dependencies are usable.
- Request IDs help correlate logs from the same request.
- Rate limiting protects expensive endpoints from accidental or abusive traffic.
- Audit logs provide accountability for configuration changes.
- Metrics and tracing would be natural next additions for production observability.

### Check yourself

Explain this chapter without looking at the code. Then trace one concrete request and identify where each concept appears in the repository.

## Study chapter 18
### HTTP fundamentals
- A browser or SDK is an HTTP client. Django is an HTTP server application behind a WSGI server.
- GET should retrieve representations. POST commonly creates resources or invokes commands. PATCH partially updates a resource. DELETE removes a resource.
- Status codes communicate categories of outcomes. 2xx means success, 4xx means the caller should change something, and 5xx means the server failed.
- JSON is a serialization format, not the database itself. DRF parses JSON request bodies into Python primitives and serializes Python data back to JSON.
- Headers carry metadata such as content type, authentication, correlation identifiers, caching directives, and tracing information.

### Django request processing
- The WSGI application receives a request from Gunicorn and Django middleware begins processing.
- URL routing resolves the incoming path to a view.
- DRF viewsets provide reusable request dispatch for REST resources.
- Serializers validate incoming primitive data and convert model objects to outgoing representations.
- Services coordinate business use cases while repositories isolate query details.

### Database fundamentals
- PostgreSQL persists relational rows and enforces constraints that application code alone cannot safely guarantee under concurrency.
- A foreign key connects one table to another. Here environments belong to projects and flags belong to environments.
- A unique constraint prevents duplicate keys within a defined scope.
- Indexes speed up selected reads at the cost of extra storage and write overhead.
- Transactions let a group of database changes commit or roll back together.

### Caching
- Redis stores data in memory and can answer repeated lookups much faster than a relational query.
- Caches introduce staleness risk, so invalidation strategy matters.
- A cache key must encode the identity of the configuration it represents.
- Versioned or namespaced keys reduce accidental collisions.
- A cache should be treated as disposable; PostgreSQL remains the authoritative source in this project.

### Background jobs
- Celery workers run tasks outside the interactive HTTP request.
- Background processing is useful for expensive or retryable work such as webhook delivery and analytics aggregation.
- A broker such as Redis carries task messages from producers to workers.
- Tasks should be designed for retries because distributed systems can deliver work more than once.
- Idempotent task design reduces damage from duplicate execution.

### Frontend state
- React renders UI from component state and props.
- An event handler reacts to a click and usually calls an API abstraction.
- The API client translates a JavaScript object into a JSON request.
- After the server responds, state updates cause React to render a new UI.
- Keeping network code outside presentation components reduces repetition.

### Rollout systems
- Percentage rollout is cohort selection, not request-level randomness.
- Stable hashing means a user can repeatedly receive the same decision.
- Increasing rollout percentage should ideally include the cohort that already had the feature.
- A kill switch must be able to override normal rollout logic quickly.
- Targeting rules should produce explainable decisions so debugging is possible.

### Operational concerns
- Health endpoints answer whether the process is alive; readiness endpoints answer whether dependencies are usable.
- Request IDs help correlate logs from the same request.
- Rate limiting protects expensive endpoints from accidental or abusive traffic.
- Audit logs provide accountability for configuration changes.
- Metrics and tracing would be natural next additions for production observability.

### Check yourself

Explain this chapter without looking at the code. Then trace one concrete request and identify where each concept appears in the repository.

## Study chapter 19
### HTTP fundamentals
- A browser or SDK is an HTTP client. Django is an HTTP server application behind a WSGI server.
- GET should retrieve representations. POST commonly creates resources or invokes commands. PATCH partially updates a resource. DELETE removes a resource.
- Status codes communicate categories of outcomes. 2xx means success, 4xx means the caller should change something, and 5xx means the server failed.
- JSON is a serialization format, not the database itself. DRF parses JSON request bodies into Python primitives and serializes Python data back to JSON.
- Headers carry metadata such as content type, authentication, correlation identifiers, caching directives, and tracing information.

### Django request processing
- The WSGI application receives a request from Gunicorn and Django middleware begins processing.
- URL routing resolves the incoming path to a view.
- DRF viewsets provide reusable request dispatch for REST resources.
- Serializers validate incoming primitive data and convert model objects to outgoing representations.
- Services coordinate business use cases while repositories isolate query details.

### Database fundamentals
- PostgreSQL persists relational rows and enforces constraints that application code alone cannot safely guarantee under concurrency.
- A foreign key connects one table to another. Here environments belong to projects and flags belong to environments.
- A unique constraint prevents duplicate keys within a defined scope.
- Indexes speed up selected reads at the cost of extra storage and write overhead.
- Transactions let a group of database changes commit or roll back together.

### Caching
- Redis stores data in memory and can answer repeated lookups much faster than a relational query.
- Caches introduce staleness risk, so invalidation strategy matters.
- A cache key must encode the identity of the configuration it represents.
- Versioned or namespaced keys reduce accidental collisions.
- A cache should be treated as disposable; PostgreSQL remains the authoritative source in this project.

### Background jobs
- Celery workers run tasks outside the interactive HTTP request.
- Background processing is useful for expensive or retryable work such as webhook delivery and analytics aggregation.
- A broker such as Redis carries task messages from producers to workers.
- Tasks should be designed for retries because distributed systems can deliver work more than once.
- Idempotent task design reduces damage from duplicate execution.

### Frontend state
- React renders UI from component state and props.
- An event handler reacts to a click and usually calls an API abstraction.
- The API client translates a JavaScript object into a JSON request.
- After the server responds, state updates cause React to render a new UI.
- Keeping network code outside presentation components reduces repetition.

### Rollout systems
- Percentage rollout is cohort selection, not request-level randomness.
- Stable hashing means a user can repeatedly receive the same decision.
- Increasing rollout percentage should ideally include the cohort that already had the feature.
- A kill switch must be able to override normal rollout logic quickly.
- Targeting rules should produce explainable decisions so debugging is possible.

### Operational concerns
- Health endpoints answer whether the process is alive; readiness endpoints answer whether dependencies are usable.
- Request IDs help correlate logs from the same request.
- Rate limiting protects expensive endpoints from accidental or abusive traffic.
- Audit logs provide accountability for configuration changes.
- Metrics and tracing would be natural next additions for production observability.

### Check yourself

Explain this chapter without looking at the code. Then trace one concrete request and identify where each concept appears in the repository.

## Study chapter 20
### HTTP fundamentals
- A browser or SDK is an HTTP client. Django is an HTTP server application behind a WSGI server.
- GET should retrieve representations. POST commonly creates resources or invokes commands. PATCH partially updates a resource. DELETE removes a resource.
- Status codes communicate categories of outcomes. 2xx means success, 4xx means the caller should change something, and 5xx means the server failed.
- JSON is a serialization format, not the database itself. DRF parses JSON request bodies into Python primitives and serializes Python data back to JSON.
- Headers carry metadata such as content type, authentication, correlation identifiers, caching directives, and tracing information.

### Django request processing
- The WSGI application receives a request from Gunicorn and Django middleware begins processing.
- URL routing resolves the incoming path to a view.
- DRF viewsets provide reusable request dispatch for REST resources.
- Serializers validate incoming primitive data and convert model objects to outgoing representations.
- Services coordinate business use cases while repositories isolate query details.

### Database fundamentals
- PostgreSQL persists relational rows and enforces constraints that application code alone cannot safely guarantee under concurrency.
- A foreign key connects one table to another. Here environments belong to projects and flags belong to environments.
- A unique constraint prevents duplicate keys within a defined scope.
- Indexes speed up selected reads at the cost of extra storage and write overhead.
- Transactions let a group of database changes commit or roll back together.

### Caching
- Redis stores data in memory and can answer repeated lookups much faster than a relational query.
- Caches introduce staleness risk, so invalidation strategy matters.
- A cache key must encode the identity of the configuration it represents.
- Versioned or namespaced keys reduce accidental collisions.
- A cache should be treated as disposable; PostgreSQL remains the authoritative source in this project.

### Background jobs
- Celery workers run tasks outside the interactive HTTP request.
- Background processing is useful for expensive or retryable work such as webhook delivery and analytics aggregation.
- A broker such as Redis carries task messages from producers to workers.
- Tasks should be designed for retries because distributed systems can deliver work more than once.
- Idempotent task design reduces damage from duplicate execution.

### Frontend state
- React renders UI from component state and props.
- An event handler reacts to a click and usually calls an API abstraction.
- The API client translates a JavaScript object into a JSON request.
- After the server responds, state updates cause React to render a new UI.
- Keeping network code outside presentation components reduces repetition.

### Rollout systems
- Percentage rollout is cohort selection, not request-level randomness.
- Stable hashing means a user can repeatedly receive the same decision.
- Increasing rollout percentage should ideally include the cohort that already had the feature.
- A kill switch must be able to override normal rollout logic quickly.
- Targeting rules should produce explainable decisions so debugging is possible.

### Operational concerns
- Health endpoints answer whether the process is alive; readiness endpoints answer whether dependencies are usable.
- Request IDs help correlate logs from the same request.
- Rate limiting protects expensive endpoints from accidental or abusive traffic.
- Audit logs provide accountability for configuration changes.
- Metrics and tracing would be natural next additions for production observability.

### Check yourself

Explain this chapter without looking at the code. Then trace one concrete request and identify where each concept appears in the repository.

