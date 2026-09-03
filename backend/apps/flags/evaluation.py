from dataclasses import dataclass
import hashlib
from typing import Any

from .models import FeatureFlag, TargetingRule

BUCKET_SCALE = 10_000

@dataclass(frozen=True)
class EvaluationContext:
    user_id: str
    attributes: dict[str, Any]

@dataclass(frozen=True)
class EvaluationResult:
    flag_key: str
    enabled: bool
    value: Any
    reason: str
    bucket: int | None
    rollout_percentage: int
    matched_rule: int | None

    def as_dict(self):
        return {
            "flag_key": self.flag_key,
            "enabled": self.enabled,
            "value": self.value,
            "reason": self.reason,
            "bucket": self.bucket,
            "rollout_percentage": self.rollout_percentage,
            "matched_rule": self.matched_rule,
        }

class StableBucketer:
    @staticmethod
    def bucket(*, project_key, environment_key, flag_key, user_id):
        identity = f"{project_key}:{environment_key}:{flag_key}:{user_id}"
        digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()
        integer = int(digest[:16], 16)
        return integer % BUCKET_SCALE

class TargetingEvaluator:
    @staticmethod
    def matches(rule: TargetingRule, attributes: dict[str, Any]) -> bool:
        actual = attributes.get(rule.attribute)
        expected = rule.comparison_value

        if rule.operator == TargetingRule.OP_EQUALS:
            return actual == expected

        if rule.operator == TargetingRule.OP_NOT_EQUALS:
            return actual != expected

        if rule.operator == TargetingRule.OP_IN:
            if not isinstance(expected, list):
                return False
            return actual in expected

        if rule.operator == TargetingRule.OP_NOT_IN:
            if not isinstance(expected, list):
                return False
            return actual not in expected

        if rule.operator == TargetingRule.OP_CONTAINS:
            if isinstance(actual, (list, tuple, set, str)):
                return expected in actual
            return False

        return False

class FeatureEvaluator:
    @classmethod
    def evaluate(cls, flag: FeatureFlag, context: EvaluationContext) -> EvaluationResult:
        if not flag.enabled:
            return EvaluationResult(
                flag_key=flag.key,
                enabled=False,
                value=flag.off_value,
                reason="FLAG_DISABLED",
                bucket=None,
                rollout_percentage=flag.rollout_percentage,
                matched_rule=None,
            )

        if flag.premium_only and not bool(context.attributes.get("premium", False)):
            return EvaluationResult(
                flag_key=flag.key,
                enabled=False,
                value=flag.off_value,
                reason="PREMIUM_REQUIRED",
                bucket=None,
                rollout_percentage=flag.rollout_percentage,
                matched_rule=None,
            )

        matched_rule = None
        matched_value = None

        for rule in flag.targeting_rules.all():
            if rule.enabled and TargetingEvaluator.matches(rule, context.attributes):
                matched_rule = rule.id
                matched_value = rule.serve_value
                break

        # An off rule is an explicit exclusion. An enabling rule selects the
        # value to serve, but the user must still pass the percentage rollout.
        if matched_rule is not None and not bool(matched_value):
            return EvaluationResult(
                flag_key=flag.key,
                enabled=False,
                value=flag.off_value,
                reason="TARGETING_RULE_MATCH",
                bucket=None,
                rollout_percentage=flag.rollout_percentage,
                matched_rule=matched_rule,
            )

        if flag.rollout_percentage <= 0:
            return EvaluationResult(
                flag_key=flag.key,
                enabled=False,
                value=flag.off_value,
                reason="ROLLOUT_ZERO",
                bucket=0,
                rollout_percentage=flag.rollout_percentage,
                matched_rule=matched_rule,
            )

        if flag.rollout_percentage >= 100:
            return EvaluationResult(
                flag_key=flag.key,
                enabled=True,
                value=matched_value if matched_rule is not None else flag.default_value,
                reason="ROLLOUT_FULL",
                bucket=0,
                rollout_percentage=flag.rollout_percentage,
                matched_rule=matched_rule,
            )

        bucket = StableBucketer.bucket(
            project_key=flag.environment.project.key,
            environment_key=flag.environment.key,
            flag_key=flag.key,
            user_id=context.user_id,
        )

        threshold = flag.rollout_percentage * 100
        enabled = bucket < threshold

        return EvaluationResult(
            flag_key=flag.key,
            enabled=enabled,
            value=(
                matched_value if matched_rule is not None else flag.default_value
            ) if enabled else flag.off_value,
            reason="ROLLOUT_MATCH" if enabled else "ROLLOUT_MISS",
            bucket=bucket,
            rollout_percentage=flag.rollout_percentage,
            matched_rule=matched_rule,
        )
