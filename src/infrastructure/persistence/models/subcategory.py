from django.db import models


class SbSubcategory(models.Model):
    cat = models.ForeignKey("persistence.SbCategory", on_delete=models.RESTRICT)
    title = models.CharField(max_length=120)
    subcat_img = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sb_subcategory"
        constraints = [
            models.UniqueConstraint(fields=["cat", "title"], name="sb_subcategory_cat_title_uniq")
        ]
        indexes = [
            models.Index(fields=["status"], name="idx_sb_subcategory_status"),
            models.Index(fields=["cat"], name="idx_sb_subcategory_cat_id"),
            models.Index(fields=["cat", "status"], name="idx_sb_subcategory_cat_status"),
        ]


