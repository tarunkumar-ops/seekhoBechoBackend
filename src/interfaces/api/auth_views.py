from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.application.dtos.auth_dtos import RequestOtpInput, VerifyOtpInput
from src.container import get_container
from src.interfaces.api.auth_serializers import RequestOtpSerializer, VerifyOtpSerializer
from src.shared.exceptions import AuthError, ValidationError
from src.interfaces.api.auth_serializers import RefreshSerializer
from src.application.dtos.auth_dtos import RefreshTokenInput


class RequestOtpView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        ser = RequestOtpSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            get_container().request_login_otp().execute(RequestOtpInput(**ser.validated_data))
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "otp_sent"}, status=status.HTTP_200_OK)


class VerifyOtpView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        ser = VerifyOtpSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            out = get_container().verify_login_otp().execute(VerifyOtpInput(**ser.validated_data))
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except AuthError as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"access": out.access, "refresh": out.refresh}, status=status.HTTP_200_OK)


class RefreshTokenView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        ser = RefreshSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            out = get_container().refresh_tokens().execute(RefreshTokenInput(**ser.validated_data))
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except AuthError as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"access": out.access, "refresh": out.refresh}, status=status.HTTP_200_OK)
