from typing import List
from django.db import models
from django.utils import timezone

from src.application.ports.banner import BannerRepositoryPort, BannerDto, MediaDto
from src.infrastructure.persistence.models import SbBanner, SbMedia


class DjangoBannerRepository(BannerRepositoryPort):
    def list_active_banners(self, *, placement: str, platform: str) -> List[BannerDto]:
        now = timezone.now()
        qs = (
            SbBanner.objects.filter(
                placement=placement,
                platform=platform,
                is_active=True,
            )
            .filter(models.Q(start_at__lte=now) | models.Q(start_at__isnull=True))
            .filter(models.Q(end_at__gte=now) | models.Q(end_at__isnull=True))
            .select_related("media")
            .order_by("-priority")[:100]
        )
        out = []
        for b in qs:
            m = b.media
            media = MediaDto(
                id=str(m.id),
                media_type=m.media_type,
                media_url=m.media_url,
                poster_url=m.poster_url,
                width=m.width,
                height=m.height,
                duration=m.duration,
            )
            out.append(
                BannerDto(
                    id=str(b.id),
                    title=b.title,
                    media=media,
                    placement=b.placement,
                    platform=b.platform,
                    target_type=b.target_type,
                    target_value=b.target_value,
                    priority=b.priority,
                )
            )
        return out

