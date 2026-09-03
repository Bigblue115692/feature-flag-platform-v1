from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class EvaluationContext:
    user_id: str
    attributes: dict[str, Any] = field(default_factory=dict)

    def as_api_user(self) -> dict[str, Any]:
        return {
            "id": self.user_id,
            **self.attributes,
        }
