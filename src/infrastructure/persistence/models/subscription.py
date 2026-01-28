from django.db import models


class SbSubscription(models.Model):
    plan_code = models.CharField(max_length=30, unique=True)
    plan_name = models.CharField(max_length=200)
    plan_short_name = models.CharField(max_length=60, null=True, blank=True)

    description = models.TextField(null=True, blank=True)
    terms = models.TextField(null=True, blank=True)

    products_per_month = models.IntegerField(default=0)
    products_per_year = models.IntegerField(default=0)
    allow_redownload = models.BooleanField(default=False)
    initial_loyalty_points = models.IntegerField(default=0)

    state = models.ForeignKey("persistence.State", on_delete=models.RESTRICT, null=True, blank=True)

    price_type = models.CharField(max_length=30, default="FIXED")
    base_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_percent = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    add_on_category_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    monthly_earning = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    total_members_in_plan = models.IntegerField(default=0)
    total_courses_in_plan = models.IntegerField(default=0)
    free_category_count = models.IntegerField(default=0)

    is_default = models.BooleanField(default=False)
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sb_subscription"
        indexes = [
            models.Index(fields=["status"], name="idx_sb_subscription_status"),
            models.Index(fields=["is_default"], name="idx_sb_subscription_is_default"),
            models.Index(fields=["state"], name="idx_sb_subscription_state_id"),
            models.Index(fields=["price_type"], name="idx_sb_subscription_price_type"),
        ]
        constraints = [
            models.CheckConstraint(condition=models.Q(products_per_month__gte=0), name="sb_subscription_products_per_month_gte_0"),
        ]


