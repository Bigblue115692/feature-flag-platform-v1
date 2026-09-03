from django.contrib import admin
from django.urls import include, path
from apps.core.views import health, ready

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health, name="health"),
    path("ready/", ready, name="ready"),
    path("api/v1/", include("apps.flags.urls")),
    path("api/v1/", include("apps.audit.urls")),
]
