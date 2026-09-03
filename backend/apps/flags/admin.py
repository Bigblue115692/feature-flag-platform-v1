from django.contrib import admin
from .models import Environment, FeatureFlag, Project, TargetingRule

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "key", "created_at")
    search_fields = ("name", "key")

@admin.register(Environment)
class EnvironmentAdmin(admin.ModelAdmin):
    list_display = ("id", "project", "name", "key", "created_at")
    list_filter = ("project",)
    search_fields = ("name", "key")

class TargetingRuleInline(admin.TabularInline):
    model = TargetingRule
    extra = 0

@admin.register(FeatureFlag)
class FeatureFlagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "key",
        "environment",
        "enabled",
        "rollout_percentage",
        "premium_only",
        "version",
    )
    list_filter = ("enabled", "premium_only", "environment")
    search_fields = ("name", "key", "description")
    inlines = [TargetingRuleInline]
