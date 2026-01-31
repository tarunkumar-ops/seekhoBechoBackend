from django.urls import path

from src.interfaces.api.auth_views import RequestOtpView, VerifyOtpView
from src.interfaces.api.auth_views import RefreshTokenView
from src.interfaces.api.geo_views import CitiesSearchView
from src.interfaces.api.user_views import UserDetailsView
from src.interfaces.api.config_views import PrefillConfigView
from src.interfaces.api.banner_views import BannerListView
from src.interfaces.api.media_views import MediaPresignView
from src.interfaces.api.media_confirm_views import ConfirmMediaView

urlpatterns = [
    path("auth/request-otp/", RequestOtpView.as_view(), name="auth-request-otp"),
    path("auth/verify-otp/", VerifyOtpView.as_view(), name="auth-verify-otp"),
    path("auth/refresh/", RefreshTokenView.as_view(), name="auth-refresh"),
    path("geo/cities/", CitiesSearchView.as_view(), name="geo-cities-search"),
    path("config/prefill/", PrefillConfigView.as_view(), name="config-prefill"),
    path("banners/", BannerListView.as_view(), name="banners-list"),
    path("media/presign/", MediaPresignView.as_view(), name="media-presign"),
    path("media/confirm/", ConfirmMediaView.as_view(), name="media-confirm"),
    path("user/me/", UserDetailsView.as_view(), name="user-me"),
]

