from django.db import transaction

from .models import AuditEvent

class AuditService:
    @staticmethod
    def record(*, entity_type, entity_id="", action, actor="", request_id="", metadata=None):
        return AuditEvent.objects.create(
            entity_type=entity_type,
            entity_id=str(entity_id or ""),
            action=action,
            actor=actor or "",
            request_id=request_id or "",
            metadata=metadata or {},
        )

    @staticmethod
    def enqueue(*, entity_type, entity_id="", action, actor="", request_id="", metadata=None):
        from .tasks import persist_audit_event

        event = {
            "entity_type": entity_type,
            "entity_id": str(entity_id or ""),
            "action": action,
            "actor": actor or "",
            "request_id": request_id or "",
            "metadata": metadata or {},
        }
        transaction.on_commit(
            lambda: persist_audit_event.apply_async(kwargs=event, queue="audit")
        )
