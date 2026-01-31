from typing import List
from django.db import models
from django.utils import timezone

from src.application.ports.banner import BannerRepositoryPort, BannerDto, MediaDto
from src.infrastructure.persistence.models import SbBanner, SbMedia
from src.shared.exceptions import ValidationError
from django.utils import timezone
from typing import Optional
from django.db import transaction


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

    def create_banner(
        self,
        *,
        title: str | None,
        media_id: str,
        placement: str,
        platform: str,
        target_type: str,
        target_value: str | None = None,
        start_at: str | None = None,
        end_at: str | None = None,
        priority: int = 0,
        is_active: bool = True,
    ) -> BannerDto:
        # validate media exists
        try:
            media = SbMedia.objects.get(pk=media_id)
        except SbMedia.DoesNotExist:
            raise ValidationError("media_id does not exist")

        # convert optional datetimes if provided
        sa = start_at
        ea = end_at

        with transaction.atomic():
            b = SbBanner.objects.create(
                title=title or "",
                media=media,
                placement=placement,
                platform=platform,
                target_type=target_type,
                target_value=target_value,
                start_at=sa,
                end_at=ea,
                priority=priority,
                is_active=is_active,
            )

        media_dto = MediaDto(
            id=str(media.id),
            media_type=media.media_type,
            media_url=media.media_url,
            poster_url=media.poster_url,
            width=media.width,
            height=media.height,
            duration=media.duration,
        )
        return BannerDto(
            id=str(b.id),
            title=b.title,
            media=media_dto,
            placement=b.placement,
            platform=b.platform,
            target_type=b.target_type,
            target_value=b.target_value,
            priority=b.priority,
        )

