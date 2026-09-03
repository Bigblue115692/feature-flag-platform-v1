# Scaling the Platform

## Starting point

V1 is a modular monolith with remote evaluation.

That is intentionally understandable.

Scaling should be driven by observed bottlenecks rather than architecture fashion.

## Stage 1: more API replicas

Django API processes are stateless enough to replicate horizontally.

Put replicas behind a load balancer.

Shared state remains in PostgreSQL and Redis.

## Stage 2: cache configuration

Feature configuration changes far less often than it is evaluated.

That asymmetry makes configuration an excellent cache candidate.

Instead of querying PostgreSQL for every evaluation:

```text
request
 -> Redis config lookup
 -> evaluate
```

On a cache miss:

```text
Redis miss
 -> PostgreSQL
 -> populate Redis
 -> evaluate
```

On mutation:

```text
update PostgreSQL
 -> invalidate/publish config version
```

## Stage 3: remove synchronous evaluation audit writes

Writing a database row for every evaluation does not scale well.

Instead:

```text
evaluation
 -> return decision immediately
 -> emit analytics event asynchronously
```

Events can be buffered and aggregated.

Administrative changes should still have strong audit durability.

## Stage 4: local SDK evaluation

Remote evaluation makes every application request depend on the flag service network path.

A high-scale platform usually pushes configuration toward SDKs.

Conceptually:

```text
Control Plane
  |
  | configuration stream/poll
  v
SDK local cache
  |
  v
local evaluation
```

Benefits:

- very low latency
- fewer network calls
- platform outage does not immediately break evaluation
- much higher aggregate throughput

Tradeoffs:

- configuration propagation delay
- SDK complexity
- multi-language parity
- cache consistency

## Stage 5: event distribution

When flags change, configuration updates must reach many SDK instances.

Possible tools:

- Redis pub/sub
- Kafka
- cloud pub/sub systems
- WebSockets / server-sent events
- long polling

The correct choice depends on delivery guarantees and scale.

## Stage 6: database scaling

PostgreSQL can handle substantial workloads before sharding is necessary.

First use:

- appropriate indexes
- connection pooling
- query optimization
- read replicas for read-heavy control-plane operations
- partitioning for large append-only tables

Shard only when concrete constraints justify the operational complexity.

## 10 million evaluations per second

At that scale, remote Django requests for every evaluation would be the wrong architecture.

The system should push config outward and perform evaluations inside application processes.

Then the control plane serves configuration changes rather than every decision.

The platform can still receive analytics asynchronously.

This is the key architectural shift:

```text
low scale:
application -> flag API -> decision

high scale:
flag control plane -> config distribution -> application SDK -> local decision
```

## Consistency

Feature flag systems often prefer fast propagation with eventual consistency rather than distributed transactions across every SDK.

A kill switch may require more aggressive propagation guarantees.

This creates an important product question:

> How quickly must a configuration change reach every evaluator?

The answer drives infrastructure.
