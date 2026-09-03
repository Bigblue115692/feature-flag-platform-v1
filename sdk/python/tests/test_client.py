import unittest

from featureflags.client import FeatureFlagClient
from featureflags.config import ClientConfig
from featureflags.context import EvaluationContext

class FakeTransport:
    def __init__(self):
        self.calls = 0

    def post_json(self, url, payload):
        self.calls += 1
        return {
            "flag_key": payload["flag_key"],
            "enabled": True,
            "value": True,
            "reason": "ROLLOUT_FULL",
        }

class ClientTests(unittest.TestCase):
    def setUp(self):
        self.transport = FakeTransport()
        self.client = FeatureFlagClient(
            ClientConfig(
                base_url="http://example.test",
                project_key="checkout",
                environment_key="production",
                cache_ttl_seconds=60,
            ),
            transport=self.transport,
        )
        self.context = EvaluationContext(
            user_id="user-1",
            attributes={"country": "US"},
        )

    def test_is_enabled(self):
        self.assertTrue(
            self.client.is_enabled("new_checkout", self.context)
        )

    def test_cache_prevents_duplicate_http_call(self):
        self.client.evaluate("new_checkout", self.context)
        self.client.evaluate("new_checkout", self.context)
        self.assertEqual(self.transport.calls, 1)
