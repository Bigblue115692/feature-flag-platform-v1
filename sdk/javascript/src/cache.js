export class InMemoryCache {
  constructor() {
    this.entries = new Map();
  }

  get(key) {
    const entry = this.entries.get(key);
    if (!entry) {
      return undefined;
    }

    if (entry.expiresAt <= Date.now()) {
      this.entries.delete(key);
      return undefined;
    }

    return entry.value;
  }

  set(key, value, ttlMs) {
    this.entries.set(key, {
      value,
      expiresAt: Date.now() + ttlMs,
    });
  }

  clear() {
    this.entries.clear();
  }
}
