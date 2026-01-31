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

    def post(self, request):
        # Admin-only creation
        if not request.user or not request.user.is_authenticated or not request.user.is_staff:
            return Response({"message": "forbidden"}, status=status.HTTP_403_FORBIDDEN)
        from src.interfaces.api.banner_create_serializers import CreateBannerRequestSerializer, CreateBannerResponseSerializer

        ser = CreateBannerRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        try:
            banner = get_container().create_banner().execute(
                title=data.get("title"),
                media_id=str(data["media_id"]),
                placement=data["placement"],
                platform=data["platform"],
                target_type=data.get("target_type", "none"),
                target_value=data.get("target_value"),
                start_at=(data.get("start_at").isoformat() if data.get("start_at") else None),
                end_at=(data.get("end_at").isoformat() if data.get("end_at") else None),
                priority=data.get("priority", 0),
                is_active=data.get("is_active", True),
            )
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        resp = CreateBannerResponseSerializer({
            "id": banner.id,
            "title": banner.title,
            "media": banner.media.__dict__,
            "placement": banner.placement,
            "platform": banner.platform,
            "target_type": banner.target_type,
            "target_value": banner.target_value,
            "priority": banner.priority,
        })
        return Response(resp.data, status=status.HTTP_201_CREATED)

