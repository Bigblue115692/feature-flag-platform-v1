from django.core.management.base import BaseCommand
from apps.flags.models import Environment, FeatureFlag, Project, TargetingRule

class Command(BaseCommand):
    help = "Create demo project, environments, feature flags, and targeting rules."

    def handle(self, *args, **options):
        project, _ = Project.objects.get_or_create(
            key="checkout",
            defaults={
                "name": "Checkout Platform",
                "description": "Demo project for progressive checkout delivery.",
            },
        )

        production, _ = Environment.objects.get_or_create(
            project=project,
            key="production",
            defaults={"name": "Production"},
        )

        staging, _ = Environment.objects.get_or_create(
            project=project,
            key="staging",
            defaults={"name": "Staging"},
        )

        new_checkout, _ = FeatureFlag.objects.get_or_create(
            environment=production,
            key="new_checkout",
            defaults={
                "name": "New Checkout",
                "description": "Progressively deliver the rewritten checkout flow.",
                "enabled": True,
                "rollout_percentage": 25,
                "premium_only": False,
                "default_value": True,
                "off_value": False,
            },
        )

        TargetingRule.objects.get_or_create(
            flag=new_checkout,
            priority=10,
            attribute="country",
            operator=TargetingRule.OP_IN,
            comparison_value=["US", "CA"],
            defaults={"serve_value": True},
        )

        FeatureFlag.objects.get_or_create(
            environment=production,
            key="premium_dashboard",
            defaults={
                "name": "Premium Dashboard",
                "enabled": True,
                "rollout_percentage": 100,
                "premium_only": True,
                "default_value": True,
                "off_value": False,
            },
        )

        FeatureFlag.objects.get_or_create(
            environment=staging,
            key="new_checkout",
            defaults={
                "name": "New Checkout",
                "enabled": True,
                "rollout_percentage": 100,
                "premium_only": False,
                "default_value": True,
                "off_value": False,
            },
        )

        self.stdout.write(self.style.SUCCESS("Demo data created."))
