from celery import shared_task
from django.utils import timezone
from apps.audit.models import AuditEvent

@shared_task
def prune_old_evaluation_audits(days=30):
    cutoff = timezone.now() - timezone.timedelta(days=days)
    deleted, _ = AuditEvent.objects.filter(
        action=AuditEvent.ACTION_EVALUATE,
        created_at__lt=cutoff,
    ).delete()
    return deleted

@shared_task
def warm_flag_cache():
    # Placeholder hook for future cache warming.
    # The service currently reads flags directly with optimized ORM queries.
    return {"status": "ok"}
