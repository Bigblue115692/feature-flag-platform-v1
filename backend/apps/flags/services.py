from django.db import transaction
from django.conf import settings

from apps.audit.models import AuditEvent
from apps.audit.services import AuditService
from .cache import FlagCache
from .evaluation import EvaluationContext, FeatureEvaluator, FlagConfiguration
from .repositories import FeatureFlagRepository

class FeatureFlagService:
    @staticmethod
    @transaction.atomic
    def create_flag(*, validated_data, actor="", request_id=""):
        flag = FeatureFlagRepository.create(**validated_data)
        AuditService.enqueue(
            entity_type="feature_flag",
            entity_id=flag.id,
            action=AuditEvent.ACTION_CREATE,
            actor=actor,
            request_id=request_id,
            metadata={"after": FeatureFlagService.snapshot(flag)},
        )
        return flag

    @staticmethod
    @transaction.atomic
    def update_flag(*, flag, validated_data, actor="", request_id=""):
        before = FeatureFlagService.snapshot(flag)
        updated = FeatureFlagRepository.update(flag, **validated_data)
        after = FeatureFlagService.snapshot(updated)

        AuditService.enqueue(
            entity_type="feature_flag",
            entity_id=updated.id,
            action=AuditEvent.ACTION_UPDATE,
            actor=actor,
            request_id=request_id,
            metadata={"before": before, "after": after},
        )

        return updated

    @staticmethod
    @transaction.atomic
    def delete_flag(*, flag, actor="", request_id=""):
        before = FeatureFlagService.snapshot(flag)
        flag_id = flag.id
        AuditService.enqueue(
            entity_type="feature_flag",
            entity_id=flag_id,
            action=AuditEvent.ACTION_DELETE,
            actor=actor,
            request_id=request_id,
            metadata={"before": before},
        )
        FeatureFlagRepository.delete(flag)

    @staticmethod
    def evaluate(*, project_key, environment_key, flag_key, user, actor="", request_id=""):
        payload = FlagCache.get(project_key, environment_key, flag_key)
        if payload is None:
            flag = FeatureFlagRepository.get_for_evaluation(
                project_key=project_key,
                environment_key=environment_key,
                flag_key=flag_key,
            )
            payload = FlagCache.serialize(flag)
            FlagCache.set(project_key, environment_key, flag_key, payload)

        flag = FlagConfiguration.from_payload(payload)

        user_id = str(user.get("id", ""))
        attributes = dict(user)
        attributes.pop("id", None)

        context = EvaluationContext(
            user_id=user_id,
            attributes=attributes,
        )
        result = FeatureEvaluator.evaluate(flag, context)

        if settings.EVALUATION_AUDIT_ENABLED:
            AuditService.enqueue(
                entity_type="feature_flag",
                entity_id=flag.id,
                action=AuditEvent.ACTION_EVALUATE,
                actor=actor or user_id,
                request_id=request_id,
                metadata={
                    "project_key": project_key,
                    "environment_key": environment_key,
                    "flag_key": flag_key,
                    "result": result.as_dict(),
                },
            )

        return result

    @staticmethod
    def snapshot(flag):
        return {
            "id": flag.id,
            "environment_id": flag.environment_id,
            "name": flag.name,
            "key": flag.key,
            "description": flag.description,
            "enabled": flag.enabled,
            "rollout_percentage": flag.rollout_percentage,
            "premium_only": flag.premium_only,
            "default_value": flag.default_value,
            "off_value": flag.off_value,
            "version": flag.version,
        }
