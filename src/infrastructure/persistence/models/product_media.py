from django.db import models


class SbProductMedia(models.Model):
    product = models.ForeignKey("persistence.SbProduct", on_delete=models.CASCADE, db_column="product_id")
    title = models.CharField(max_length=200, null=True, blank=True)
    product_img = models.CharField(max_length=500)
    image_type = models.CharField(max_length=50)
    sort_order = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sb_product_media"
        indexes = [
            models.Index(fields=["product"], name="idx_sb_prod_media_product_id"),
            models.Index(fields=["status"], name="idx_sb_product_media_status"),
            models.Index(fields=["image_type"], name="idx_sb_product_media_type"),
            models.Index(fields=["product", "sort_order"], name="idx_sb_product_media_sort"),
        ]


