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
