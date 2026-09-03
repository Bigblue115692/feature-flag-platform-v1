import json
import time
import urllib.error
import urllib.request

from .exceptions import FeatureFlagTransportError

class HttpTransport:
    def __init__(self, timeout_seconds=2.0, retries=2):
        self.timeout_seconds = timeout_seconds
        self.retries = retries

    def post_json(self, url: str, payload: dict) -> dict:
        body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            url,
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "User-Agent": "feature-flag-python-sdk/1.0",
            },
        )

        last_error = None

        for attempt in range(self.retries + 1):
            try:
                with urllib.request.urlopen(
                    request,
                    timeout=self.timeout_seconds,
                ) as response:
                    raw = response.read().decode("utf-8")
                    return json.loads(raw)

            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                last_error = exc
                if attempt < self.retries:
                    time.sleep(0.05 * (2 ** attempt))
                    continue
                break

        raise FeatureFlagTransportError(
            f"Feature flag API request failed after {self.retries + 1} attempts: {last_error}"
        )
