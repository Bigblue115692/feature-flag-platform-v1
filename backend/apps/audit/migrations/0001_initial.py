from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AuditEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("entity_type", models.CharField(max_length=64)),
                ("entity_id", models.CharField(blank=True, max_length=128)),
                ("action", models.CharField(choices=[("create", "Create"), ("update", "Update"), ("delete", "Delete"), ("evaluate", "Evaluate")], max_length=32)),
                ("actor", models.CharField(blank=True, max_length=255)),
                ("request_id", models.CharField(blank=True, max_length=128)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
