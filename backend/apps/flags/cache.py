from django.conf import settings
from django.core.cache import cache

class FlagCache:
    PREFIX = "flag-eval"

    @classmethod
    def key(cls, project_key, environment_key, flag_key):
        return f"{cls.PREFIX}:{project_key}:{environment_key}:{flag_key}"

    @classmethod
    def get(cls, project_key, environment_key, flag_key):
        return cache.get(cls.key(project_key, environment_key, flag_key))

    @classmethod
    def set(cls, project_key, environment_key, flag_key, payload, timeout=None):
        cache.set(
            cls.key(project_key, environment_key, flag_key),
            payload,
            timeout=timeout or settings.FLAG_CACHE_TIMEOUT,
        )

    @staticmethod
    def serialize(flag):
        return {
            "id": flag.id,
            "project_key": flag.environment.project.key,
            "environment_key": flag.environment.key,
            "key": flag.key,
            "enabled": flag.enabled,
            "rollout_percentage": flag.rollout_percentage,
            "premium_only": flag.premium_only,
            "default_value": flag.default_value,
            "off_value": flag.off_value,
            "version": flag.version,
            "targeting_rules": [
                {
                    "id": rule.id,
                    "attribute": rule.attribute,
                    "operator": rule.operator,
                    "comparison_value": rule.comparison_value,
                    "enabled": rule.enabled,
                    "serve_value": rule.serve_value,
                }
                for rule in flag.targeting_rules.all()
            ],
        }

    @classmethod
    def invalidate(cls, flag):
        cls.invalidate_by_keys(
            flag.environment.project.key,
            flag.environment.key,
            flag.key,
        )

    @classmethod
    def invalidate_by_keys(cls, project_key, environment_key, flag_key):
        cache.delete(cls.key(project_key, environment_key, flag_key))
