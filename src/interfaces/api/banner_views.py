from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from src.container import get_container
from src.interfaces.api.banner_serializers import BannerSerializer


class BannerListView(APIView):
    """
    GET /api/banners/?placement=HOME_TOP&platform=android
    Returns active banners (by placement + platform), ordered by priority desc.
    """

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        placement = request.query_params.get("placement")
        platform = request.query_params.get("platform")
        if not placement or not platform:
            return Response({"message": "placement and platform are required"}, status=status.HTTP_400_BAD_REQUEST)
        out = get_container().list_banners().execute(placement=placement, platform=platform)
        ser = BannerSerializer(out, many=True)
        return Response({"banners": ser.data}, status=status.HTTP_200_OK)

