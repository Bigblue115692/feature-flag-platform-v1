from django.test import TestCase
from rest_framework.test import APIClient

from apps.flags.models import Environment, FeatureFlag, Project

class FeatureFlagApiTests(TestCase):
    def setUp(self):
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

    def test_evaluate(self):
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
