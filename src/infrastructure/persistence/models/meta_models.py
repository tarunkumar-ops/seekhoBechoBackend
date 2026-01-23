from django.db import models


class Country(models.Model):
    title = models.CharField(max_length=120, unique=True)
    iso2 = models.CharField(max_length=2, null=True, blank=True, unique=True)
    iso3 = models.CharField(max_length=3, null=True, blank=True, unique=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sb_country"


class InterestedPlatform(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.CharField(max_length=140, null=True, blank=True, unique=True)
    sort_order = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sb_interested_platform"
        indexes = [
            models.Index(fields=["status"], name="idx_sb_interst_platform_status"),
            models.Index(fields=["sort_order"], name="idx_sb_interst_platform_sort"),
        ]


class Language(models.Model):
    title = models.CharField(max_length=120, unique=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sb_language"
        indexes = [
            models.Index(fields=["status"], name="idx_sb_language_status"),
        ]


class State(models.Model):
    title = models.CharField(max_length=120)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    country = models.ForeignKey("persistence.Country", on_delete=models.RESTRICT)

    class Meta:
        db_table = "sb_state"
        constraints = [
            models.UniqueConstraint(fields=["country", "title"], name="sb_state_country_title_uniq"),
        ]
        indexes = [
            models.Index(fields=["country"], name="idx_sb_state_country_id"),
            models.Index(fields=["title"], name="idx_sb_state_title"),
        ]


class Occupation(models.Model):
    title = models.CharField(max_length=120, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "occupations"
        indexes = [
            models.Index(fields=["title"], name="idx_occupations_title"),
        ]


class City(models.Model):
    country_name = models.CharField(max_length=120)
    state_name = models.CharField(max_length=120)
    title = models.CharField(max_length=120)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    country = models.ForeignKey("persistence.Country", on_delete=models.RESTRICT)
    state = models.ForeignKey("persistence.State", on_delete=models.RESTRICT)

    class Meta:
        db_table = "sb_city"
        constraints = [
            models.UniqueConstraint(fields=["state", "title"], name="sb_city_state_title_uniq"),
        ]
        indexes = [
            models.Index(fields=["state", "title"], name="idx_sb_city_state_title"),
        ]

