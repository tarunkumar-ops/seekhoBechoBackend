from django.db import models


class SbProduct(models.Model):
    product_code = models.CharField(max_length=30, unique=True)
    product_name = models.CharField(max_length=200)

    cat = models.ForeignKey("persistence.SbCategory", on_delete=models.RESTRICT, db_column="cat_id")
    subcat = models.ForeignKey("persistence.SbSubcategory", on_delete=models.RESTRICT, null=True, blank=True, db_column="subcat_id")

    sku_code = models.CharField(max_length=80, unique=True, null=True, blank=True)
    hsn_code = models.CharField(max_length=30, null=True, blank=True)

    description = models.TextField(null=True, blank=True)

    no_of_compartments = models.IntegerField(null=True, blank=True)
    no_of_pockets = models.IntegerField(null=True, blank=True)

    occasion = models.CharField(max_length=120, null=True, blank=True)
    product_color = models.CharField(max_length=120, null=True, blank=True)
    material_used_for = models.CharField(max_length=150, null=True, blank=True)
    brand = models.CharField(max_length=150, null=True, blank=True)

    selling_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    offer_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    height = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    breadth = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    length = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sb_products"
        constraints = [
            models.CheckConstraint(condition=models.Q(selling_price__gte=0), name="sb_products_selling_price_gte_0"),
            models.CheckConstraint(condition=(models.Q(offer_price__isnull=True) | models.Q(offer_price__gte=0)), name="sb_products_offer_price_gte_0"),
        ]
        indexes = [
            models.Index(fields=["cat"], name="idx_sb_products_cat_id"),
            models.Index(fields=["subcat"], name="idx_sb_products_subcat_id"),
            models.Index(fields=["status"], name="idx_sb_products_status"),
            models.Index(fields=["created_at"], name="idx_sb_products_created_at"),
            models.Index(fields=["selling_price"], name="idx_sb_products_price"),
            models.Index(fields=["offer_price"], name="idx_sb_products_offer_price"),
            models.Index(fields=["product_name"], name="idx_sb_products_name"),
        ]


