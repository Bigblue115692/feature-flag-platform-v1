from django.contrib import admin
from .models import AuditEvent

@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = ("id", "entity_type", "entity_id", "action", "actor", "created_at")
    list_filter = ("entity_type", "action")
    search_fields = ("entity_id", "actor", "request_id")
