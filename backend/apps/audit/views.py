from rest_framework import viewsets
from .models import AuditEvent
from .serializers import AuditEventSerializer

class AuditEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditEvent.objects.all()
    serializer_class = AuditEventSerializer
    filterset_fields = ["entity_type", "entity_id", "action"]
