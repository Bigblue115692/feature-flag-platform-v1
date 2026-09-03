from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import EnvironmentViewSet, FeatureFlagViewSet, ProjectViewSet, evaluate

router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="project")
router.register("environments", EnvironmentViewSet, basename="environment")
router.register("flags", FeatureFlagViewSet, basename="flag")

urlpatterns = [
    path("evaluate/", evaluate, name="evaluate"),
]
urlpatterns += router.urls
