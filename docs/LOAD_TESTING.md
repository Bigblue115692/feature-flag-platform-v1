# Load Testing

The evaluation load test uses k6's constant-arrival-rate executor so the target
request rate remains independent of response latency. It exercises the complete
remote path: Nginx, Django, PostgreSQL configuration reads, deterministic
bucketing, and synchronous audit writes.

## Live dashboard

Start the application stack first:

```bash
docker compose up -d
```

Run the safe 15-second smoke test:

```bash
docker compose --profile loadtest run --rm --service-ports k6
```

While the test is running, open:

```text
http://localhost:5665
```

The dashboard displays throughput, latency, checks, and failures in real time.
At the end of the run, a self-contained report is written to:

```text
load-tests/results/latest.html
```

## Five-minute baseline

After the smoke test passes, run 50 evaluations per second for five minutes:

```bash
K6_RATE=50 K6_DURATION=5m docker compose --profile loadtest run --rm --service-ports k6
```

This creates approximately 15,000 evaluation audit rows. Use only local or
purpose-built test environments, not production.

## Configuration

The following environment variables can adjust a run:

- `K6_RATE`: evaluations started per second (default `10`)
- `K6_DURATION`: test duration (default `15s`)
- `K6_PRE_ALLOCATED_VUS`: workers reserved before the run (default `25`)
- `K6_MAX_VUS`: maximum workers k6 may allocate (default `200`)

The test sends unique premium US users so the seeded targeting rule participates
and the 25% stable rollout produces both enabled and disabled decisions.

## Initial thresholds

- More than 99% of checks must pass.
- HTTP failures must remain below 1%.
- p95 response latency must remain below 250 ms.
- p99 response latency must remain below 500 ms.
- No scheduled iterations may be dropped.

These are initial correctness and reliability thresholds, not final performance
claims. Record the hardware, Docker resource limits, commit, rate, and duration
with every published result.

## Published results

- [2026-09-03 V1 remote evaluation baseline](benchmarks/2026-09-03-v1-baseline/README.md)
- [2026-09-04 V1 maximum-throughput ramp](benchmarks/2026-09-04-throughput-ramp/README.md)
