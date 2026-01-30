from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("persistence", "0004_user_interested_platform_and_remove_platform"),
    ]

    operations = [
        migrations.CreateModel(
            name="SbMedia",
            fields=[
                ("id", models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ("media_type", models.CharField(max_length=10)),
                ("media_url", models.URLField(max_length=1000)),
                ("poster_url", models.URLField(blank=True, max_length=1000, null=True)),
                ("width", models.PositiveIntegerField(blank=True, null=True)),
                ("height", models.PositiveIntegerField(blank=True, null=True)),
                ("duration", models.FloatField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"db_table": "sb_media"},
        ),
        migrations.CreateModel(
            name="SbBanner",
            fields=[
                ("id", models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ("title", models.CharField(blank=True, max_length=200)),
                ("placement", models.CharField(max_length=40)),
                ("platform", models.CharField(max_length=20)),
                ("target_type", models.CharField(default="none", max_length=30)),
                ("target_value", models.CharField(blank=True, max_length=1000, null=True)),
                ("start_at", models.DateTimeField(blank=True, null=True)),
                ("end_at", models.DateTimeField(blank=True, null=True)),
                ("priority", models.IntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "media",
                    models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to="persistence.SbMedia"),
                ),
            ],
            options={"db_table": "sb_banner", "ordering": ["-priority", "-created_at"]},
        ),
        migrations.AddIndex(
            model_name="sbbanner",
            index=models.Index(fields=["placement"], name="idx_sb_banner_placement"),
        ),
        migrations.AddIndex(
            model_name="sbbanner",
            index=models.Index(fields=["platform"], name="idx_sb_banner_platform"),
        ),
        migrations.AddIndex(
            model_name="sbbanner",
            index=models.Index(fields=["is_active"], name="idx_sb_banner_active"),
        ),
        migrations.AddIndex(
            model_name="sbmedia",
            index=models.Index(fields=["media_type"], name="idx_sb_media_type"),
        ),
    ]

