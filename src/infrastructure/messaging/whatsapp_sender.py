import logging

from twilio.rest import Client

from src.application.ports.otp import OtpSenderPort

logger = logging.getLogger(__name__)


class TwilioWhatsAppOtpSender(OtpSenderPort):
    def __init__(self, *, account_sid: str, auth_token: str, from_whatsapp: str) -> None:
        self._client = Client(account_sid, auth_token)
        self._from = from_whatsapp

    def send_whatsapp_otp(self, *, to_phone: str, code: str) -> None:
        # Twilio expects WhatsApp addresses like: "whatsapp:+201234567890"
        self._client.messages.create(
            from_=f"whatsapp:{self._from}",
            to=f"whatsapp:{to_phone}",
            body=f"Your login code is: {code}",
        )


class DevLoggingWhatsAppOtpSender(OtpSenderPort):
    """
    For local/dev/testing: avoids external calls. Logs OTP to server console.
    """

    def send_whatsapp_otp(self, *, to_phone: str, code: str) -> None:
        logger.info("DEV OTP for %s is %s", to_phone, code)

