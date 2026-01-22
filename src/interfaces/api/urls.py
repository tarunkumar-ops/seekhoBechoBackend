from django.urls import path

from src.interfaces.api.auth_views import RequestOtpView, VerifyOtpView

urlpatterns = [
    path("auth/request-otp/", RequestOtpView.as_view(), name="auth-request-otp"),
    path("auth/verify-otp/", VerifyOtpView.as_view(), name="auth-verify-otp"),
]

