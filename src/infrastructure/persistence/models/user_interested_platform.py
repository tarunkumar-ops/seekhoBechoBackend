from django.db import models


class SbUserInterestedPlatform(models.Model):
    user = models.ForeignKey("persistence.SbUser", on_delete=models.RESTRICT, db_column="user_id")
    platform = models.ForeignKey("persistence.InterestedPlatform", on_delete=models.RESTRICT, db_column="platform_id")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sb_user_interested_platform"
        constraints = [
            models.UniqueConstraint(fields=["user", "platform"], name="sb_user_platform_user_platform_uniq")
        ]

