from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from src.container import get_container
from src.interfaces.api.geo_serializers import StateSerializer, CitySerializer


class StateListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # For now restrict to India (ISO2 = 'IN')
        out = get_container().list_states().execute(country_iso2="IN")
        ser = StateSerializer(out, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class CityListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, state_id: int):
        out = get_container().list_cities().execute(state_id=int(state_id))
        ser = CitySerializer(out, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

