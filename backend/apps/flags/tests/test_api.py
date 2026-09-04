from django.test import TestCase, override_settings
from django.core.cache import cache
from unittest.mock import patch
from rest_framework.test import APIClient

from apps.audit.models import AuditEvent
from apps.flags.models import Environment, FeatureFlag, Project

class FeatureFlagApiTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.project = Project.objects.create(name="Checkout", key="checkout")
        self.environment = Environment.objects.create(
            project=self.project,
            name="Production",
            key="production",
        )
        self.flag = FeatureFlag.objects.create(
            environment=self.environment,
            name="New Checkout",
            key="new_checkout",
            enabled=True,
            rollout_percentage=100,
            default_value=True,
            off_value=False,
        )

    def tearDown(self):
        cache.clear()

    def test_list_flags(self):
        response = self.client.get("/api/v1/flags/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_patch_flag(self):
        response = self.client.patch(
            f"/api/v1/flags/{self.flag.id}/",
            {"rollout_percentage": 50},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.flag.refresh_from_db()
        self.assertEqual(self.flag.rollout_percentage, 50)
        self.assertEqual(self.flag.version, 2)

    @override_settings(EVALUATION_AUDIT_ENABLED=True)
    @patch("apps.audit.tasks.persist_audit_event.apply_async")
    def test_evaluate(self, apply_async):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(
                "/api/v1/evaluate/",
                {
                    "project_key": "checkout",
                    "environment_key": "production",
                    "flag_key": "new_checkout",
                    "user": {"id": "user-1"},
                },
                format="json",
            )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["enabled"])
        apply_async.assert_called_once()
        self.assertEqual(
            apply_async.call_args.kwargs["kwargs"]["action"],
            AuditEvent.ACTION_EVALUATE,
        )
        self.assertEqual(apply_async.call_args.kwargs["queue"], "audit")

    @override_settings(EVALUATION_AUDIT_ENABLED=False)
    def test_evaluate_can_skip_audit_event(self):
        response = self.client.post(
            "/api/v1/evaluate/",
            {
                "project_key": "checkout",
                "environment_key": "production",
                "flag_key": "new_checkout",
                "user": {"id": "user-1"},
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            AuditEvent.objects.filter(action=AuditEvent.ACTION_EVALUATE).exists()
        )

    @override_settings(EVALUATION_AUDIT_ENABLED=False)
    def test_second_evaluation_uses_cached_configuration_without_database_queries(self):
        cache.clear()
        request = {
            "project_key": "checkout",
            "environment_key": "production",
            "flag_key": "new_checkout",
            "user": {"id": "user-1"},
        }

        first = self.client.post("/api/v1/evaluate/", request, format="json")
        self.assertEqual(first.status_code, 200)

        with self.assertNumQueries(0):
            second = self.client.post("/api/v1/evaluate/", request, format="json")

        self.assertEqual(second.status_code, 200)
        self.assertEqual(first.json(), second.json())

    @override_settings(EVALUATION_AUDIT_ENABLED=False)
    def test_flag_update_invalidates_cached_configuration_after_commit(self):
        cache.clear()
        request = {
            "project_key": "checkout",
            "environment_key": "production",
            "flag_key": "new_checkout",
            "user": {"id": "user-1"},
        }
        self.client.post("/api/v1/evaluate/", request, format="json")
        cache_key = "flag-eval:checkout:production:new_checkout"
        self.assertIsNotNone(cache.get(cache_key))

        with patch("apps.audit.tasks.persist_audit_event.apply_async"):
            with self.captureOnCommitCallbacks(execute=True):
                response = self.client.patch(
                    f"/api/v1/flags/{self.flag.id}/",
                    {"rollout_percentage": 50},
                    format="json",
                )

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(cache.get(cache_key))
