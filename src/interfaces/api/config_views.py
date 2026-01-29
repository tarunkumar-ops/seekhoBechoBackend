from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from src.container import get_container
from src.interfaces.api.config_serializers import OccupationSerializer, InterestedPlatformSerializer


class PrefillConfigView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        out = get_container().get_prefill_config().execute()
        occ_ser = OccupationSerializer(out["occupations"], many=True)
        plat_ser = InterestedPlatformSerializer(out["interested_platforms"], many=True)
        return Response({"occupations": occ_ser.data, "interested_platforms": plat_ser.data}, status=status.HTTP_200_OK)

