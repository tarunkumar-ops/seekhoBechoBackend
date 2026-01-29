from django.db import models


class SbSubscriptionBenefits(models.Model):
    subscription = models.ForeignKey("persistence.SbSubscription", on_delete=models.CASCADE, db_column="subscription_id")
    benefit_type = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    sort_order = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sb_subscription_benefits"
        indexes = [
            models.Index(fields=["subscription"], name="idx_sb_sub_benef_subscrip_id"),
            models.Index(fields=["benefit_type"], name="idx_sb_sub_benefits_type"),
            models.Index(fields=["status"], name="idx_sb_sub_benefits_status"),
            models.Index(fields=["subscription", "sort_order"], name="idx_sb_sub_benefits_sort"),
        ]


