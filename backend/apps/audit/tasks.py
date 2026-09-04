from celery import shared_task

from .services import AuditService


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    max_retries=8,
    acks_late=True,
    reject_on_worker_lost=True,
    ignore_result=True,
)
def persist_audit_event(self, **event):
    audit = AuditService.record(**event)
    return audit.id
