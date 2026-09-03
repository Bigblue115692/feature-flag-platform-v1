from rest_framework import serializers
from .models import Environment, FeatureFlag, Project, TargetingRule

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "key", "description", "created_at", "updated_at"]

class EnvironmentSerializer(serializers.ModelSerializer):
    project_key = serializers.CharField(source="project.key", read_only=True)

    class Meta:
        model = Environment
        fields = [
            "id",
            "project",
            "project_key",
            "name",
            "key",
            "description",
            "created_at",
            "updated_at",
        ]

class TargetingRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetingRule
        fields = [
            "id",
            "flag",
            "priority",
            "attribute",
            "operator",
            "comparison_value",
            "enabled",
            "serve_value",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["flag"]

class FeatureFlagSerializer(serializers.ModelSerializer):
    project_key = serializers.CharField(source="environment.project.key", read_only=True)
    environment_key = serializers.CharField(source="environment.key", read_only=True)
    targeting_rules = TargetingRuleSerializer(many=True, read_only=True)

    class Meta:
        model = FeatureFlag
        fields = [
            "id",
            "environment",
            "project_key",
            "environment_key",
            "name",
            "key",
            "description",
            "enabled",
            "rollout_percentage",
            "premium_only",
            "default_value",
            "off_value",
            "version",
            "targeting_rules",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["version"]

    def validate_rollout_percentage(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Rollout percentage must be between 0 and 100.")
        return value

class EvaluationUserSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255)
    premium = serializers.BooleanField(required=False)
    country = serializers.CharField(required=False, allow_blank=True)
    plan = serializers.CharField(required=False, allow_blank=True)

    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        for key, raw in data.items():
            if key not in value:
                value[key] = raw
        return value

class EvaluationRequestSerializer(serializers.Serializer):
    project_key = serializers.SlugField()
    environment_key = serializers.SlugField()
    flag_key = serializers.SlugField()
    user = EvaluationUserSerializer()

class EvaluationResponseSerializer(serializers.Serializer):
    flag_key = serializers.CharField()
    enabled = serializers.BooleanField()
    value = serializers.JSONField()
    reason = serializers.CharField()
    bucket = serializers.IntegerField(allow_null=True)
    rollout_percentage = serializers.IntegerField()
    matched_rule = serializers.IntegerField(allow_null=True)
