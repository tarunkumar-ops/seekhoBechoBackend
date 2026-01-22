import re

from src.shared.exceptions import ValidationError


E164_REGEX = re.compile(r"^\+[1-9]\d{6,14}$")


def normalize_e164(phone: str) -> str:
    """
    Very small phone normalizer for E.164.
    Expect input like: +201234567890
    """
    if phone is None:
        raise ValidationError("phone is required")
    phone = phone.strip()
    if not E164_REGEX.match(phone):
        raise ValidationError("phone must be in E.164 format, e.g. +201234567890")
    return phone

