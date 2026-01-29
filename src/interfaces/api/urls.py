from django.urls import path

from src.interfaces.api.auth_views import RequestOtpView, VerifyOtpView
from src.interfaces.api.auth_views import RefreshTokenView
from src.interfaces.api.geo_views import CitiesWithStateView, CitiesSearchView
from src.interfaces.api.user_views import UserDetailsView

urlpatterns = [
    path("auth/request-otp/", RequestOtpView.as_view(), name="auth-request-otp"),
    path("auth/verify-otp/", VerifyOtpView.as_view(), name="auth-verify-otp"),
    path("auth/refresh/", RefreshTokenView.as_view(), name="auth-refresh"),
    path("geo/cities/<int:state_id>/", CitiesWithStateView.as_view(), name="geo-cities-with-state"),
    path("geo/cities/", CitiesSearchView.as_view(), name="geo-cities-search"),
    path("user/me/", UserDetailsView.as_view(), name="user-me"),
]

