import http from "k6/http";
import exec from "k6/execution";
import { check } from "k6";
import { Counter, Rate } from "k6/metrics";

const enabledEvaluations = new Counter("evaluations_enabled");
const disabledEvaluations = new Counter("evaluations_disabled");
const rolloutEnabled = new Rate("rollout_enabled");
const targetingMatched = new Rate("targeting_matched");

const rate = Number.parseInt(__ENV.RATE || "10", 10);
const preAllocatedVUs = Number.parseInt(__ENV.PRE_ALLOCATED_VUS || "25", 10);
const maxVUs = Number.parseInt(__ENV.MAX_VUS || "200", 10);

export const options = {
  discardResponseBodies: false,
  scenarios: {
    evaluation_load: {
      executor: "constant-arrival-rate",
      rate,
      timeUnit: "1s",
      duration: __ENV.DURATION || "15s",
      preAllocatedVUs,
      maxVUs,
      gracefulStop: "10s",
    },
  },
  thresholds: {
    checks: ["rate>0.99"],
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<250", "p(99)<500"],
    dropped_iterations: ["count==0"],
  },
};

export default function () {
  const iteration = exec.scenario.iterationInTest;
  const userId = `k6-user-${iteration}`;
  const payload = JSON.stringify({
    project_key: __ENV.PROJECT_KEY || "checkout",
    environment_key: __ENV.ENVIRONMENT_KEY || "production",
    flag_key: __ENV.FLAG_KEY || "new_checkout",
    user: {
      id: userId,
      premium: true,
      country: "US",
      load_test: true,
    },
  });

  const response = http.post(`${__ENV.BASE_URL}/api/v1/evaluate/`, payload, {
    headers: {
      "Content-Type": "application/json",
      Host: "localhost",
      "X-Actor": "k6-load-test",
    },
    tags: { endpoint: "evaluate" },
  });

  let body = null;
  try {
    body = response.json();
  } catch (_) {
    // The checks below report malformed or non-JSON responses.
  }

  const valid = check(response, {
    "evaluation returned 200": (res) => res.status === 200,
    "evaluation returned JSON": () => body !== null,
    "evaluation returned a boolean decision": () =>
      body !== null && typeof body.enabled === "boolean",
    "targeting rule participated": () =>
      body !== null && body.matched_rule !== null,
    "partial rollout returned a bucket": () =>
      body !== null && Number.isInteger(body.bucket),
  });

  if (!valid || body === null) {
    return;
  }

  targetingMatched.add(body.matched_rule !== null);
  rolloutEnabled.add(body.enabled);
  if (body.enabled) {
    enabledEvaluations.add(1);
  } else {
    disabledEvaluations.add(1);
  }
}
