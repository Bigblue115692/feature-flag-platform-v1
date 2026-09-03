from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Project(TimestampedModel):
    name = models.CharField(max_length=120)
    key = models.SlugField(max_length=80, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Environment(TimestampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="environments")
    name = models.CharField(max_length=120)
    key = models.SlugField(max_length=80)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["project__name", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["project", "key"],
                name="unique_environment_key_per_project",
            )
        ]

    def __str__(self):
        return f"{self.project.key}/{self.key}"

class FeatureFlag(TimestampedModel):
    environment = models.ForeignKey(
        Environment,
        on_delete=models.CASCADE,
        related_name="feature_flags",
    )
    name = models.CharField(max_length=160)
    key = models.SlugField(max_length=100)
    description = models.TextField(blank=True)

    enabled = models.BooleanField(default=False)
    rollout_percentage = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    premium_only = models.BooleanField(default=False)
    default_value = models.JSONField(default=False)
    off_value = models.JSONField(default=False)

    version = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["environment__project__name", "environment__name", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["environment", "key"],
                name="unique_flag_key_per_environment",
            )
        ]
        indexes = [
            models.Index(fields=["environment", "key"]),
            models.Index(fields=["enabled", "rollout_percentage"]),
        ]

    def __str__(self):
        return f"{self.environment}:{self.key}"

class TargetingRule(TimestampedModel):
    OP_EQUALS = "equals"
    OP_NOT_EQUALS = "not_equals"
    OP_IN = "in"
    OP_NOT_IN = "not_in"
    OP_CONTAINS = "contains"

    OPERATOR_CHOICES = [
        (OP_EQUALS, "Equals"),
        (OP_NOT_EQUALS, "Not equals"),
        (OP_IN, "In"),
        (OP_NOT_IN, "Not in"),
        (OP_CONTAINS, "Contains"),
    ]

    flag = models.ForeignKey(
        FeatureFlag,
        on_delete=models.CASCADE,
        related_name="targeting_rules",
    )
    priority = models.PositiveIntegerField(default=100)
    attribute = models.CharField(max_length=100)
    operator = models.CharField(max_length=32, choices=OPERATOR_CHOICES)
    comparison_value = models.JSONField()
    enabled = models.BooleanField(default=True)
    serve_value = models.JSONField(default=True)

    class Meta:
        ordering = ["priority", "id"]
        indexes = [
            models.Index(fields=["flag", "priority"]),
        ]

    def __str__(self):
        return f"{self.flag.key}:{self.attribute}:{self.operator}"
