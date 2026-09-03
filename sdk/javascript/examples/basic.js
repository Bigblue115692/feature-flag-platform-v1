import { EvaluationContext, FeatureFlagClient } from "../src/index.js";

const client = new FeatureFlagClient({
  baseUrl: "http://localhost",
  projectKey: "checkout",
  environmentKey: "production",
});

const context = new EvaluationContext("user-107", {
  premium: true,
  country: "US",
  plan: "pro",
});

const enabled = await client.isEnabled("new_checkout", context);

console.log({ enabled });
