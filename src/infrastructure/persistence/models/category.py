from django.db import models


class SbCategory(models.Model):
    title = models.CharField(max_length=120, unique=True)
    cat_img = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category_for = models.CharField(max_length=100, null=True, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sb_category"
        indexes = [models.Index(fields=["status"], name="idx_sb_category_status")]


