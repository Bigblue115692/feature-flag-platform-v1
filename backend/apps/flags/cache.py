import json
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
    def set(cls, project_key, environment_key, flag_key, payload, timeout=300):
        cache.set(
            cls.key(project_key, environment_key, flag_key),
            payload,
            timeout=timeout,
        )

    @classmethod
    def invalidate(cls, flag):
        cache.delete(
            cls.key(
                flag.environment.project.key,
                flag.environment.key,
                flag.key,
            )
        )
