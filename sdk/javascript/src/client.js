import { InMemoryCache } from "./cache.js";

export class FeatureFlagClient {
  constructor({
    baseUrl,
    projectKey,
    environmentKey,
    timeoutMs = 2000,
    retries = 2,
    cacheTtlMs = 5000,
    cache = new InMemoryCache(),
    fetchImpl = globalThis.fetch,
  }) {
    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.projectKey = projectKey;
    this.environmentKey = environmentKey;
    this.timeoutMs = timeoutMs;
    this.retries = retries;
    this.cacheTtlMs = cacheTtlMs;
    this.cache = cache;
    this.fetchImpl = fetchImpl;
  }

  async evaluate(flagKey, context) {
    const cacheKey = this.cacheKey(flagKey, context);
    const cached = this.cache.get(cacheKey);

    if (cached !== undefined) {
      return cached;
    }

    const payload = {
      project_key: this.projectKey,
      environment_key: this.environmentKey,
      flag_key: flagKey,
      user: context.toApiUser(),
    };

    const result = await this.postJson(
      `${this.baseUrl}/api/v1/evaluate/`,
      payload,
    );

    this.cache.set(cacheKey, result, this.cacheTtlMs);
    return result;
  }

  async isEnabled(flagKey, context, defaultValue = false) {
    try {
      const result = await this.evaluate(flagKey, context);
      return Boolean(result.enabled);
    } catch {
      return defaultValue;
    }
  }

  async value(flagKey, context, defaultValue = null) {
    try {
      const result = await this.evaluate(flagKey, context);
      return result.value ?? defaultValue;
    } catch {
      return defaultValue;
    }
  }

  async postJson(url, payload) {
    let lastError = null;

    for (let attempt = 0; attempt <= this.retries; attempt += 1) {
      const controller = new AbortController();
      const timeout = setTimeout(
        () => controller.abort(),
        this.timeoutMs,
      );

      try {
        const response = await this.fetchImpl(url, {
          method: "POST",
          signal: controller.signal,
          headers: {
            "Content-Type": "application/json",
            "User-Agent": "feature-flag-js-sdk/1.0",
          },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        return await response.json();
      } catch (error) {
        lastError = error;
        if (attempt < this.retries) {
          await new Promise((resolve) =>
            setTimeout(resolve, 50 * (2 ** attempt)),
          );
        }
      } finally {
        clearTimeout(timeout);
      }
    }

    throw lastError || new Error("Feature flag request failed");
  }

  cacheKey(flagKey, context) {
    return JSON.stringify([
      flagKey,
      context.userId,
      context.attributes,
    ]);
  }
}
