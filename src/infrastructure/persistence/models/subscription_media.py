from django.db import models


class SbSubscriptionMedia(models.Model):
    subscription = models.ForeignKey("persistence.SbSubscription", on_delete=models.CASCADE, db_column="subscription_id")
    media_group = models.CharField(max_length=40)
    title = models.CharField(max_length=200, null=True, blank=True)
    file_path = models.CharField(max_length=500)
    file_type = models.CharField(max_length=30, null=True, blank=True)
    sort_order = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sb_subscription_media"
        indexes = [
            models.Index(fields=["subscription"], name="idx_sb_sub_media_subscrip_id"),
            models.Index(fields=["media_group"], name="idx_sb_sub_media_group"),
            models.Index(fields=["status"], name="idx_sb_sub_media_status"),
            models.Index(fields=["subscription", "media_group", "sort_order"], name="idx_sb_sub_media_sort"),
        ]


