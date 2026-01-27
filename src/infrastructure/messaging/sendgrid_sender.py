import logging
import os
from typing import Any

import requests

from django.conf import settings

from src.application.ports.otp import OtpSenderPort

logger = logging.getLogger(__name__)


class SendGridEmailOtpSender(OtpSenderPort):
    def __init__(self, *, api_key: str | None = None, from_email: str | None = None) -> None:
        self._api_key = api_key or getattr(settings, "SENDGRID_API_KEY", None)
        self._from_email = from_email or getattr(settings, "SENDGRID_FROM_EMAIL", None)
        # Template id for OTP emails. Can be overridden in settings.
        self._template_id = getattr(
            settings, "SENDGRID_OTP_TEMPLATE_ID", "d-fa12fc6a251140fa9b3d51dba5e54734"
        )

    def send_whatsapp_otp(self, *, to_phone: str, code: str, expires_in_minutes: int) -> None:
        raise NotImplementedError("SendGridEmailOtpSender does not send WhatsApp messages")

    def send_email_otp(self, *, to_email: str, code: str, expires_in_minutes: int) -> None:
        if not self._api_key or not self._from_email:
            logger.warning("SendGrid not configured; skipping email to %s", to_email)
            return
        url = "https://api.sendgrid.com/v3/mail/send"
        # Use dynamic template if template id is provided. Send dynamic_template_data with variables:
        # OTP_CODE and OTP_EXPIRY
        payload = {
            "from": {"email": self._from_email},
            "personalizations": [
                {
                    "to": [{"email": to_email}],
                    "dynamic_template_data": {"OTP_CODE": code, "OTP_EXPIRY": expires_in_minutes},
                }
            ],
            "template_id": self._template_id,
        }
        headers = {"Authorization": f"Bearer {self._api_key}", "Content-Type": "application/json"}
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=5)
            if resp.status_code >= 400:
                logger.error("SendGrid send failed: %s %s", resp.status_code, resp.text)
            else:
                logger.info("SendGrid email OTP sent to %s using template %s", to_email, self._template_id)
        except Exception as e:
            logger.exception("SendGrid request failed: %s", e)

