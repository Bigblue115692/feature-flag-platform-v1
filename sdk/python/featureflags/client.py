import json
from hashlib import sha256

from .cache import InMemoryCache
from .config import ClientConfig
from .context import EvaluationContext
from .transport import HttpTransport

class FeatureFlagClient:
    def __init__(
        self,
        config: ClientConfig,
        transport: HttpTransport | None = None,
        cache: InMemoryCache | None = None,
    ):
        self.config = config
        self.transport = transport or HttpTransport(
            timeout_seconds=config.timeout_seconds,
            retries=config.retries,
        )
        self.cache = cache or InMemoryCache()

    def evaluate(self, flag_key: str, context: EvaluationContext) -> dict:
        cache_key = self._cache_key(flag_key, context)
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        payload = {
            "project_key": self.config.project_key,
            "environment_key": self.config.environment_key,
            "flag_key": flag_key,
            "user": context.as_api_user(),
        }

        result = self.transport.post_json(
            f"{self.config.normalized_base_url()}/api/v1/evaluate/",
            payload,
        )

        self.cache.set(
            cache_key,
            result,
            ttl_seconds=self.config.cache_ttl_seconds,
        )
        return result

    def is_enabled(
        self,
        flag_key: str,
        context: EvaluationContext,
        default: bool = False,
    ) -> bool:
        try:
            result = self.evaluate(flag_key, context)
            return bool(result.get("enabled", default))
        except Exception:
            return default

    def value(
        self,
        flag_key: str,
        context: EvaluationContext,
        default=None,
    ):
        try:
            result = self.evaluate(flag_key, context)
            return result.get("value", default)
        except Exception:
            return default

    def _cache_key(self, flag_key: str, context: EvaluationContext) -> str:
        material = json.dumps(
            {
                "flag_key": flag_key,
                "user_id": context.user_id,
                "attributes": context.attributes,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        return sha256(material.encode("utf-8")).hexdigest()
