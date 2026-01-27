from typing import Optional

from src.application.ports.otp import OtpSenderPort


class CompositeOtpSender(OtpSenderPort):
    def __init__(self, *, whatsapp_sender: OtpSenderPort | None = None, email_sender: OtpSenderPort | None = None) -> None:
        self._whatsapp = whatsapp_sender
        self._email = email_sender

    def send_whatsapp_otp(self, *, to_phone: str, code: str, expires_in_minutes: int) -> None:
        if not self._whatsapp:
            raise RuntimeError("WhatsApp sender not configured")
        return self._whatsapp.send_whatsapp_otp(to_phone=to_phone, code=code, expires_in_minutes=expires_in_minutes)

    def send_email_otp(self, *, to_email: str, code: str, expires_in_minutes: int) -> None:
        if not self._email:
            raise RuntimeError("Email sender not configured")
        return self._email.send_email_otp(to_email=to_email, code=code, expires_in_minutes=expires_in_minutes)

