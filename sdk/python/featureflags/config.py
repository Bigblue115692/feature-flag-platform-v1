from dataclasses import dataclass

@dataclass(frozen=True)
class ClientConfig:
    base_url: str
    project_key: str
    environment_key: str
    timeout_seconds: float = 2.0
    cache_ttl_seconds: float = 5.0
    retries: int = 2

    def normalized_base_url(self) -> str:
        return self.base_url.rstrip("/")
