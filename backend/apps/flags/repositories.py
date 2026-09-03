from django.db.models import Prefetch
from .models import Environment, FeatureFlag, Project, TargetingRule

class ProjectRepository:
    @staticmethod
    def list():
        return Project.objects.all()

    @staticmethod
    def get_by_key(key):
        return Project.objects.get(key=key)

class EnvironmentRepository:
    @staticmethod
    def list():
        return Environment.objects.select_related("project").all()

    @staticmethod
    def get_by_keys(project_key, environment_key):
        return Environment.objects.select_related("project").get(
            project__key=project_key,
            key=environment_key,
        )

class FeatureFlagRepository:
    @staticmethod
    def list():
        return (
            FeatureFlag.objects
            .select_related("environment", "environment__project")
            .prefetch_related(
                Prefetch(
                    "targeting_rules",
                    queryset=TargetingRule.objects.filter(enabled=True).order_by("priority", "id"),
                )
            )
            .all()
        )

    @staticmethod
    def get(flag_id):
        return (
            FeatureFlagRepository.list()
            .get(pk=flag_id)
        )

    @staticmethod
    def get_for_evaluation(project_key, environment_key, flag_key):
        return (
            FeatureFlagRepository.list()
            .get(
                environment__project__key=project_key,
                environment__key=environment_key,
                key=flag_key,
            )
        )

    @staticmethod
    def create(**validated_data):
        return FeatureFlag.objects.create(**validated_data)

    @staticmethod
    def update(instance, **validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.version += 1
        instance.save()
        return instance

    @staticmethod
    def delete(instance):
        instance.delete()
