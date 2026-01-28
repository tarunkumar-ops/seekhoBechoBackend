from django.test import Client, TestCase, override_settings

from src.infrastructure.persistence.models import LoginOtp
from src.infrastructure.persistence.repositories.otp_repository import DjangoLoginOtpRepository


@override_settings(TWILIO_ENABLED=False, OTP_SECRET="test-secret")
class OtpAuthFlowTests(TestCase):
    def test_request_and_verify_otp_returns_tokens(self):
        c = Client()
        phone = "+201234567890"

        r1 = c.post("/api/auth/request-otp/", data={"phone": phone}, content_type="application/json")
        self.assertEqual(r1.status_code, 200)

        otp = LoginOtp.objects.filter(phone=phone).order_by("-created_at").first()
        self.assertIsNotNone(otp)

        # Create a known OTP code (the request endpoint creates a random one)
        repo = DjangoLoginOtpRepository(secret="test-secret")
        repo.create_login_otp(phone=phone, code="123456", ttl_seconds=300)

        r2 = c.post(
            "/api/auth/verify-otp/",
            data={"phone": phone, "code": "123456"},
            content_type="application/json",
        )
        self.assertEqual(r2.status_code, 200)
        body = r2.json()
        self.assertIn("access_token", body)
        self.assertIn("refresh_token", body)

