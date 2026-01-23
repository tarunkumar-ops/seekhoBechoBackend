from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RequestOtpInput:
    phone: str


@dataclass(frozen=True)
class VerifyOtpInput:
    phone: str
    code: str


@dataclass(frozen=True)
class VerifyOtpOutput:
    access: str
    refresh: str


@dataclass(frozen=True)
class RefreshTokenInput:
    refresh: str


@dataclass(frozen=True)
class RefreshTokenOutput:
    access: str
    refresh: str

