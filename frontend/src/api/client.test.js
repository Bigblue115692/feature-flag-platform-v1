import { afterEach, describe, expect, it, vi } from "vitest";
import { api } from "./client";

describe("api client", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("loads flags", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => ({
        ok: true,
        text: async () => JSON.stringify([{ id: 1, key: "new_checkout" }]),
      })),
    );

    const flags = await api.listFlags();

    expect(flags).toHaveLength(1);
    expect(flags[0].key).toBe("new_checkout");
  });
});
