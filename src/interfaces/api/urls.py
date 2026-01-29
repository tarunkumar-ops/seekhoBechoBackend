from django.urls import path

from src.interfaces.api.auth_views import RequestOtpView, VerifyOtpView
from src.interfaces.api.auth_views import RefreshTokenView
from src.interfaces.api.geo_views import CitiesSearchView
from src.interfaces.api.user_views import UserDetailsView
from src.interfaces.api.config_views import PrefillConfigView

urlpatterns = [
    path("auth/request-otp/", RequestOtpView.as_view(), name="auth-request-otp"),
    path("auth/verify-otp/", VerifyOtpView.as_view(), name="auth-verify-otp"),
    path("auth/refresh/", RefreshTokenView.as_view(), name="auth-refresh"),
    path("geo/cities/", CitiesSearchView.as_view(), name="geo-cities-search"),
    path("config/prefill/", PrefillConfigView.as_view(), name="config-prefill"),
    path("user/me/", UserDetailsView.as_view(), name="user-me"),
]

