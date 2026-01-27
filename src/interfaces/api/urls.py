from django.urls import path

from src.interfaces.api.auth_views import RequestOtpView, VerifyOtpView
from src.interfaces.api.auth_views import RefreshTokenView
from src.interfaces.api.geo_views import StateListView, CityListView
from src.interfaces.api.user_views import UserDetailsView

urlpatterns = [
    path("auth/request-otp/", RequestOtpView.as_view(), name="auth-request-otp"),
    path("auth/verify-otp/", VerifyOtpView.as_view(), name="auth-verify-otp"),
    path("auth/refresh/", RefreshTokenView.as_view(), name="auth-refresh"),
    path("geo/states/", StateListView.as_view(), name="geo-states"),
    path("geo/states/<int:state_id>/cities/", CityListView.as_view(), name="geo-state-cities"),
    path("user/me/", UserDetailsView.as_view(), name="user-me"),
]

