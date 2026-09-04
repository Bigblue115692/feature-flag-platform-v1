from django.test import TestCase

from apps.audit.models import AuditEvent
from apps.audit.tasks import persist_audit_event


class AuditTaskTests(TestCase):
    def test_persist_audit_event_writes_to_database(self):
        audit_id = persist_audit_event.run(
            entity_type="feature_flag",
            entity_id="7",
            action=AuditEvent.ACTION_EVALUATE,
            actor="user-1",
            request_id="request-1",
            metadata={"enabled": True},
        )

        audit = AuditEvent.objects.get(id=audit_id)
        self.assertEqual(audit.entity_id, "7")
        self.assertEqual(audit.metadata, {"enabled": True})
