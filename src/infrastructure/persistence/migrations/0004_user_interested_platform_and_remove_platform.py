from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("persistence", "0003_alter_loginotp_phone_sbcategory_sbsubcategory_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="sbuser",
            name="platform",
        ),
        migrations.RemoveField(
            model_name="sbuser",
            name="platform_name",
        ),
        migrations.CreateModel(
            name="SbUserInterestedPlatform",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="persistence.SbUser",
                        db_column="user_id",
                    ),
                ),
                (
                    "platform",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="persistence.InterestedPlatform",
                        db_column="platform_id",
                    ),
                ),
            ],
            options={"db_table": "sb_user_interested_platform"},
        ),
        migrations.AddConstraint(
            model_name="sbuserinterestedplatform",
            constraint=models.UniqueConstraint(
                fields=("user", "platform"), name="sb_user_platform_user_platform_uniq"
            ),
        ),
    ]

