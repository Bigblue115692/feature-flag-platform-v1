from dataclasses import dataclass
import threading
import time
from typing import Any

@dataclass
class CacheEntry:
    value: Any
    expires_at: float

class InMemoryCache:
    def __init__(self):
        self._entries: dict[str, CacheEntry] = {}
        self._lock = threading.Lock()

    def get(self, key: str):
        now = time.monotonic()
        with self._lock:
            entry = self._entries.get(key)
            if entry is None:
                return None
            if entry.expires_at <= now:
                self._entries.pop(key, None)
                return None
            return entry.value

    def set(self, key: str, value, ttl_seconds: float):
        with self._lock:
            self._entries[key] = CacheEntry(
                value=value,
                expires_at=time.monotonic() + ttl_seconds,
            )

    def clear(self):
        with self._lock:
            self._entries.clear()
