import hashlib
from typing import Any
from .models import FeatureFlag
from .schemas import EvaluationResponse, UserContext

BUCKET_COUNT = 10_000


def stable_bucket(project_key: str, environment_key: str, flag_key: str, user_id: str) -> int:
    material = f"{project_key}:{environment_key}:{flag_key}:{user_id}".encode()
    digest = hashlib.sha256(material).digest()
    numeric = int.from_bytes(digest[:8], "big")
    return numeric % BUCKET_COUNT


def _lookup(user: UserContext, attribute: str) -> Any:
    if attribute == "id":
        return user.id
    if attribute == "premium":
        return user.premium
    return user.attributes.get(attribute)


def _matches(user: UserContext, rule: dict) -> bool:
    actual = _lookup(user, rule["attribute"])
    expected = rule["value"]
    op = rule["operator"]

    if op == "equals":
        return actual == expected
    if op == "not_equals":
        return actual != expected
    if op == "in":
        return actual in expected if isinstance(expected, list) else False
    if op == "not_in":
        return actual not in expected if isinstance(expected, list) else True
    if op == "contains":
        return expected in actual if isinstance(actual, (str, list, tuple, set)) else False
    return False


def evaluate_flag(project_key: str, environment_key: str, flag: FeatureFlag, user: UserContext):
    if not flag.enabled:
        return EvaluationResponse(flag_key=flag.key, enabled=False, reason="flag_disabled")

    if flag.premium_only and not user.premium:
        return EvaluationResponse(flag_key=flag.key, enabled=False, reason="premium_required")

    for rule in flag.targeting_rules or []:
        if not _matches(user, rule):
            return EvaluationResponse(
                flag_key=flag.key,
                enabled=False,
                reason=f"targeting_rule_failed:{rule['attribute']}",
            )

    bucket = stable_bucket(project_key, environment_key, flag.key, user.id)
    threshold = int((flag.rollout_percentage / 100) * BUCKET_COUNT)

    if bucket >= threshold:
        return EvaluationResponse(
            flag_key=flag.key,
            enabled=False,
            reason="outside_rollout",
            bucket=bucket,
            rollout_percentage=flag.rollout_percentage,
        )

    return EvaluationResponse(
        flag_key=flag.key,
        enabled=True,
        reason="rollout_match",
        bucket=bucket,
        rollout_percentage=flag.rollout_percentage,
    )
