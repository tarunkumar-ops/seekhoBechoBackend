from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from src.container import get_container
from src.interfaces.api.media_serializers import MediaPresignRequestSerializer, MediaPresignResponseSerializer


class MediaPresignView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ser = MediaPresignRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        file_name = ser.validated_data["file_name"]
        content_type = ser.validated_data["content_type"]
        media_type = ser.validated_data["media_type"]

        result = get_container().presign_media().execute(file_name=file_name, content_type=content_type, media_type=media_type)
        res_ser = MediaPresignResponseSerializer(result.__dict__)
        return Response(res_ser.data, status=status.HTTP_200_OK)

