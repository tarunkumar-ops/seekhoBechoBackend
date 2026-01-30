from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RequestOtpInput:
    phone: str | None = None
    email: str | None = None


@dataclass(frozen=True)
class VerifyOtpInput:
    phone: str | None = None
    email: str | None = None
    code: str = ""


@dataclass(frozen=True)
class VerifyOtpOutput:
    access: str
    refresh: str
    new_user: bool
    is_profile_complete: bool


@dataclass(frozen=True)
class RefreshTokenInput:
    refresh: str


@dataclass(frozen=True)
class RefreshTokenOutput:
    access: str
    refresh: str


@dataclass(frozen=True)
class UserDetailsOutput:
    id: int
    user_code: str | None
    full_name: str | None
    whatsapp_number: str | None
    email: str | None
    country_id: int | None
    state_id: int | None
    city_id: int | None
    occupation_id: int | None
    language_id: int | None
    country_name: str | None
    state_name: str | None
    city_name: str | None
    # platform_name removed; use interested_platforms list instead
    occupation_name: str | None
    language_name: str | None
    budget_to_invest: str | None
    gender: str | None
    status: bool | None
    interested_platforms: list[dict] | None = None


@dataclass(frozen=True)
class UpdateUserInput:
    full_name: str | None = None
    email: str | None = None
    whatsapp_number: str | None = None
    country_id: int | None = None
    state_id: int | None = None
    city_id: int | None = None
    platform_ids: list[int] | None = None
    occupation_id: int | None = None
    language_id: int | None = None
    budget_to_invest: str | None = None
    gender: str | None = None

