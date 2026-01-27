from __future__ import annotations

import time
from typing import Optional

from celery import current_app as celery_app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@celery_app.task(bind=True, max_retries=5, acks_late=True)
def send_login_otp_task(self, *, phone: Optional[str] = None, email: Optional[str] = None, otp: str, expires_minutes: int = 5):
    """
    Celery task to send login OTP via WhatsApp or Email using the project's configured senders.
    Retries on exception with exponential backoff.
    """
    try:
        # import container lazily to avoid importing Django apps at module import time
        from src.container import get_container  # local import
        container = get_container()
        sender = container._otp_sender  # composition root provides configured sender
        if phone:
            # phone may need normalization on caller; use as-is
            sender.send_whatsapp_otp(to_phone=phone, code=otp, expires_in_minutes=expires_minutes)
            logger.info("Dispatched WhatsApp OTP to %s", phone)
        elif email:
            sender.send_email_otp(to_email=email, code=otp, expires_in_minutes=expires_minutes)
            logger.info("Dispatched Email OTP to %s", email)
        else:
            raise ValueError("Either phone or email must be provided to send_login_otp_task")
    except Exception as exc:
        # exponential backoff (cap at 5 minutes)
        retries = self.request.retries if hasattr(self.request, "retries") else 0
        countdown = min(300, (2 ** retries) * 5)
        logger.exception("send_login_otp_task failed, retrying in %s seconds", countdown)
        raise self.retry(exc=exc, countdown=countdown)
