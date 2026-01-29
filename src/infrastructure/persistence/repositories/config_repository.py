from typing import List

from src.application.ports.config import ConfigRepositoryPort, OccupationDto, PlatformDto
from src.infrastructure.persistence.models import Occupation, InterestedPlatform


class DjangoConfigRepository(ConfigRepositoryPort):
    def list_occupations(self) -> List[OccupationDto]:
        qs = Occupation.objects.filter(is_active=True).order_by("title")
        return [OccupationDto(id=int(o.id), title=o.title) for o in qs]

    def list_interested_platforms(self) -> List[PlatformDto]:
        qs = InterestedPlatform.objects.filter(status=True).order_by("title")
        return [PlatformDto(id=int(p.id), title=p.title) for p in qs]

