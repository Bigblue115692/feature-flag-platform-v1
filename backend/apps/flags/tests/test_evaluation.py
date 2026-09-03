from django.test import TestCase

from apps.flags.evaluation import EvaluationContext, FeatureEvaluator, StableBucketer
from apps.flags.models import Environment, FeatureFlag, Project, TargetingRule

class StableBucketerTests(TestCase):
    def test_same_identity_produces_same_bucket(self):
        kwargs = {
            "project_key": "checkout",
            "environment_key": "production",
            "flag_key": "new_checkout",
            "user_id": "user-123",
        }
        first = StableBucketer.bucket(**kwargs)
        second = StableBucketer.bucket(**kwargs)
        self.assertEqual(first, second)

    def test_bucket_is_within_expected_range(self):
        bucket = StableBucketer.bucket(
            project_key="project",
            environment_key="production",
            flag_key="flag",
            user_id="user",
        )
        self.assertGreaterEqual(bucket, 0)
        self.assertLess(bucket, 10_000)

class FeatureEvaluatorTests(TestCase):
    def setUp(self):
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
            rollout_percentage=25,
            default_value=True,
            off_value=False,
        )

    def context(self, user_id="u1", **attributes):
        return EvaluationContext(user_id=user_id, attributes=attributes)

    def test_disabled_flag_is_off(self):
        self.flag.enabled = False
        self.flag.save()

        result = FeatureEvaluator.evaluate(self.flag, self.context())
        self.assertFalse(result.enabled)
        self.assertEqual(result.reason, "FLAG_DISABLED")

    def test_premium_only_rejects_non_premium(self):
        self.flag.premium_only = True
        self.flag.rollout_percentage = 100
        self.flag.save()

        result = FeatureEvaluator.evaluate(
            self.flag,
            self.context(premium=False),
        )
        self.assertFalse(result.enabled)
        self.assertEqual(result.reason, "PREMIUM_REQUIRED")

    def test_premium_only_accepts_premium(self):
        self.flag.premium_only = True
        self.flag.rollout_percentage = 100
        self.flag.save()

        result = FeatureEvaluator.evaluate(
            self.flag,
            self.context(premium=True),
        )
        self.assertTrue(result.enabled)

    def test_zero_rollout_is_off(self):
        self.flag.rollout_percentage = 0
        self.flag.save()

        result = FeatureEvaluator.evaluate(self.flag, self.context())
        self.assertFalse(result.enabled)
        self.assertEqual(result.reason, "ROLLOUT_ZERO")

    def test_full_rollout_is_on(self):
        self.flag.rollout_percentage = 100
        self.flag.save()

        result = FeatureEvaluator.evaluate(self.flag, self.context())
        self.assertTrue(result.enabled)
        self.assertEqual(result.reason, "ROLLOUT_FULL")

    def test_targeting_rule_does_not_bypass_zero_rollout(self):
        self.flag.rollout_percentage = 0
        self.flag.save()

        rule = TargetingRule.objects.create(
            flag=self.flag,
            priority=1,
            attribute="country",
            operator=TargetingRule.OP_EQUALS,
            comparison_value="US",
            serve_value=True,
        )

        flag = FeatureFlag.objects.prefetch_related("targeting_rules").get(pk=self.flag.pk)
        result = FeatureEvaluator.evaluate(
            flag,
            self.context(country="US"),
        )

        self.assertFalse(result.enabled)
        self.assertEqual(result.reason, "ROLLOUT_ZERO")
        self.assertEqual(result.matched_rule, rule.id)

    def test_targeting_rule_match_still_uses_percentage_bucket(self):
        rule = TargetingRule.objects.create(
            flag=self.flag,
            priority=1,
            attribute="country",
            operator=TargetingRule.OP_EQUALS,
            comparison_value="US",
            serve_value=True,
        )
        flag = FeatureFlag.objects.prefetch_related("targeting_rules").get(pk=self.flag.pk)

        matching_user = next(
            f"user-{index}"
            for index in range(10_000)
            if StableBucketer.bucket(
                project_key="checkout",
                environment_key="production",
                flag_key="new_checkout",
                user_id=f"user-{index}",
            ) < 2_500
        )
        missing_user = next(
            f"user-{index}"
            for index in range(10_000)
            if StableBucketer.bucket(
                project_key="checkout",
                environment_key="production",
                flag_key="new_checkout",
                user_id=f"user-{index}",
            ) >= 2_500
        )

        match = FeatureEvaluator.evaluate(flag, self.context(matching_user, country="US"))
        miss = FeatureEvaluator.evaluate(flag, self.context(missing_user, country="US"))

        self.assertTrue(match.enabled)
        self.assertEqual(match.reason, "ROLLOUT_MATCH")
        self.assertIsNotNone(match.bucket)
        self.assertEqual(match.matched_rule, rule.id)

        self.assertFalse(miss.enabled)
        self.assertEqual(miss.reason, "ROLLOUT_MISS")
        self.assertIsNotNone(miss.bucket)
        self.assertEqual(miss.matched_rule, rule.id)

    def test_targeting_rule_can_explicitly_serve_off_without_rollout(self):
        self.flag.rollout_percentage = 100
        self.flag.save()
        rule = TargetingRule.objects.create(
            flag=self.flag,
            priority=1,
            attribute="country",
            operator=TargetingRule.OP_EQUALS,
            comparison_value="US",
            serve_value=False,
        )
        flag = FeatureFlag.objects.prefetch_related("targeting_rules").get(pk=self.flag.pk)

        result = FeatureEvaluator.evaluate(flag, self.context(country="US"))

        self.assertFalse(result.enabled)
        self.assertEqual(result.reason, "TARGETING_RULE_MATCH")
        self.assertIsNone(result.bucket)
        self.assertEqual(result.matched_rule, rule.id)
