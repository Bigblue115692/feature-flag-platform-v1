from django.db import migrations, models
import django.db.models.deletion
import django.core.validators

class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=120)),
                ("key", models.SlugField(max_length=80, unique=True)),
                ("description", models.TextField(blank=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Environment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=120)),
                ("key", models.SlugField(max_length=80)),
                ("description", models.TextField(blank=True)),
                ("project", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="environments", to="flags.project")),
            ],
            options={"ordering": ["project__name", "name"]},
        ),
        migrations.CreateModel(
            name="FeatureFlag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=160)),
                ("key", models.SlugField(max_length=100)),
                ("description", models.TextField(blank=True)),
                ("enabled", models.BooleanField(default=False)),
                ("rollout_percentage", models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ("premium_only", models.BooleanField(default=False)),
                ("default_value", models.JSONField(default=False)),
                ("off_value", models.JSONField(default=False)),
                ("version", models.PositiveIntegerField(default=1)),
                ("environment", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="feature_flags", to="flags.environment")),
            ],
        ),
        migrations.CreateModel(
            name="TargetingRule",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("priority", models.PositiveIntegerField(default=100)),
                ("attribute", models.CharField(max_length=100)),
                ("operator", models.CharField(choices=[("equals", "Equals"), ("not_equals", "Not equals"), ("in", "In"), ("not_in", "Not in"), ("contains", "Contains")], max_length=32)),
                ("comparison_value", models.JSONField()),
                ("enabled", models.BooleanField(default=True)),
                ("serve_value", models.JSONField(default=True)),
                ("flag", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="targeting_rules", to="flags.featureflag")),
            ],
        ),
        migrations.AddConstraint(
            model_name="environment",
            constraint=models.UniqueConstraint(fields=("project", "key"), name="unique_environment_key_per_project"),
        ),
        migrations.AddConstraint(
            model_name="featureflag",
            constraint=models.UniqueConstraint(fields=("environment", "key"), name="unique_flag_key_per_environment"),
        ),
    ]
