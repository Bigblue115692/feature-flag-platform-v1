import { describe, expect, it, vi } from "vitest";
import { EvaluationContext } from "../src/context.js";
import { FeatureFlagClient } from "../src/client.js";

describe("FeatureFlagClient", () => {
  it("evaluates a flag", async () => {
    const fetchImpl = vi.fn(async () => ({
      ok: true,
      json: async () => ({
        enabled: true,
        value: true,
        reason: "ROLLOUT_FULL",
      }),
    }));

    const client = new FeatureFlagClient({
      baseUrl: "http://example.test",
      projectKey: "checkout",
      environmentKey: "production",
      fetchImpl,
    });

    const context = new EvaluationContext("user-1");

    const enabled = await client.isEnabled("new_checkout", context);

    expect(enabled).toBe(true);
    expect(fetchImpl).toHaveBeenCalledTimes(1);
  });
});
