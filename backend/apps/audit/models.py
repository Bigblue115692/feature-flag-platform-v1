from django.db import models

class AuditEvent(models.Model):
    ACTION_CREATE = "create"
    ACTION_UPDATE = "update"
    ACTION_DELETE = "delete"
    ACTION_EVALUATE = "evaluate"

    ACTION_CHOICES = [
        (ACTION_CREATE, "Create"),
        (ACTION_UPDATE, "Update"),
        (ACTION_DELETE, "Delete"),
        (ACTION_EVALUATE, "Evaluate"),
    ]

    entity_type = models.CharField(max_length=64)
    entity_id = models.CharField(max_length=128, blank=True)
    action = models.CharField(max_length=32, choices=ACTION_CHOICES)
    actor = models.CharField(max_length=255, blank=True)
    request_id = models.CharField(max_length=128, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["entity_type", "entity_id"]),
            models.Index(fields=["action", "created_at"]),
        ]

    def __str__(self):
        return f"{self.entity_type}:{self.entity_id}:{self.action}"
