from django.db import connection
from django.http import JsonResponse
from django.core.cache import cache

def health(request):
    return JsonResponse({"status": "ok"})

def ready(request):
    checks = {"database": False, "cache": False}

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        checks["database"] = True
    except Exception:
        checks["database"] = False

    try:
        cache.set("readiness-check", "ok", timeout=10)
        checks["cache"] = cache.get("readiness-check") == "ok"
    except Exception:
        checks["cache"] = False

    status = 200 if all(checks.values()) else 503
    return JsonResponse({"status": "ready" if status == 200 else "not_ready", "checks": checks}, status=status)
