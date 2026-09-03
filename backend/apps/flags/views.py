from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from .models import Environment, FeatureFlag, Project, TargetingRule
from .serializers import (
    EnvironmentSerializer,
    EvaluationRequestSerializer,
    EvaluationResponseSerializer,
    FeatureFlagSerializer,
    ProjectSerializer,
    TargetingRuleSerializer,
)
from .services import FeatureFlagService

def actor_from_request(request):
    if getattr(request, "user", None) and request.user.is_authenticated:
        return request.user.get_username()
    return request.headers.get("X-Actor", "anonymous")

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class EnvironmentViewSet(viewsets.ModelViewSet):
    queryset = Environment.objects.select_related("project").all()
    serializer_class = EnvironmentSerializer

class FeatureFlagViewSet(viewsets.ModelViewSet):
    queryset = (
        FeatureFlag.objects
        .select_related("environment", "environment__project")
        .prefetch_related("targeting_rules")
        .all()
    )
    serializer_class = FeatureFlagSerializer

    def perform_create(self, serializer):
        flag = FeatureFlagService.create_flag(
            validated_data=serializer.validated_data,
            actor=actor_from_request(self.request),
            request_id=getattr(self.request, "request_id", ""),
        )
        serializer.instance = flag

    def perform_update(self, serializer):
        flag = FeatureFlagService.update_flag(
            flag=self.get_object(),
            validated_data=serializer.validated_data,
            actor=actor_from_request(self.request),
            request_id=getattr(self.request, "request_id", ""),
        )
        serializer.instance = flag

    def perform_destroy(self, instance):
        FeatureFlagService.delete_flag(
            flag=instance,
            actor=actor_from_request(self.request),
            request_id=getattr(self.request, "request_id", ""),
        )

    @action(detail=True, methods=["post"], url_path="targeting-rules")
    def create_targeting_rule(self, request, pk=None):
        flag = self.get_object()
        serializer = TargetingRuleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rule = TargetingRule.objects.create(flag=flag, **serializer.validated_data)
        return Response(TargetingRuleSerializer(rule).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path="evaluate")
    def evaluate(self, request):
        serializer = EvaluationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = FeatureFlagService.evaluate(
            **serializer.validated_data,
            actor=actor_from_request(request),
            request_id=getattr(request, "request_id", ""),
        )
        response = EvaluationResponseSerializer(result.as_dict())
        return Response(response.data)

@api_view(["POST"])
def evaluate(request):
    serializer = EvaluationRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    result = FeatureFlagService.evaluate(
        **serializer.validated_data,
        actor=actor_from_request(request),
        request_id=getattr(request, "request_id", ""),
    )
    response = EvaluationResponseSerializer(result.as_dict())
    return Response(response.data)
