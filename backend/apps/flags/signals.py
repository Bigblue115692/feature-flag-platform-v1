from django.db import transaction
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from .cache import FlagCache
from .models import FeatureFlag, TargetingRule


def invalidate_flag_after_commit(flag):
    project_key = flag.environment.project.key
    environment_key = flag.environment.key
    flag_key = flag.key
    transaction.on_commit(
        lambda: FlagCache.invalidate_by_keys(project_key, environment_key, flag_key)
    )


@receiver(pre_save, sender=FeatureFlag)
def remember_previous_feature_flag_key(sender, instance, **kwargs):
    if not instance.pk:
        instance._previous_cache_coordinates = None
        return

    previous = (
        FeatureFlag.objects
        .select_related("environment", "environment__project")
        .filter(pk=instance.pk)
        .first()
    )
    if previous is not None:
        instance._previous_cache_coordinates = (
            previous.environment.project.key,
            previous.environment.key,
            previous.key,
        )


@receiver([post_save, post_delete], sender=FeatureFlag)
def invalidate_feature_flag(sender, instance, **kwargs):
    invalidate_flag_after_commit(instance)
    previous = getattr(instance, "_previous_cache_coordinates", None)
    if previous is not None:
        transaction.on_commit(lambda: FlagCache.invalidate_by_keys(*previous))


@receiver([post_save, post_delete], sender=TargetingRule)
def invalidate_targeting_rule(sender, instance, **kwargs):
    invalidate_flag_after_commit(instance.flag)
