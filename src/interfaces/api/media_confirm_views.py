from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from src.container import get_container
from src.interfaces.api.media_confirm_serializers import ConfirmMediaRequestSerializer, ConfirmMediaResponseSerializer
from src.shared.exceptions import ValidationError


class ConfirmMediaView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ser = ConfirmMediaRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            out = get_container().confirm_media().execute(
                media_type=ser.validated_data["media_type"],
                media_url=ser.validated_data["media_url"],
                poster_url=ser.validated_data.get("poster_url"),
                width=ser.validated_data.get("width"),
                height=ser.validated_data.get("height"),
                duration=ser.validated_data.get("duration"),
            )
        except ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        resp = ConfirmMediaResponseSerializer(out.__dict__)
        return Response(resp.data, status=status.HTTP_201_CREATED)

