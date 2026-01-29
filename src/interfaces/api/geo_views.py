from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from src.container import get_container
from src.interfaces.api.geo_serializers import StateSerializer, CitySerializer


class CitiesWithStateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, state_id: int):
        # Deprecated; keep for backward compatibility
        state, cities = get_container().list_cities_with_state().execute(state_id=int(state_id))
        if state is None:
            return Response({"message": "state not found"}, status=status.HTTP_404_NOT_FOUND)
        state_ser = StateSerializer(state)
        city_ser = CitySerializer(cities, many=True)
        return Response({"state": state_ser.data, "cities": city_ser.data}, status=status.HTTP_200_OK)


class CitiesSearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        q = request.query_params.get("q")
        city_id = request.query_params.get("city_id")
        if city_id is not None:
            try:
                city_id = int(city_id)
            except ValueError:
                return Response({"message": "invalid city_id"}, status=status.HTTP_400_BAD_REQUEST)
        result = get_container().list_cities_search().execute(q=q, city_id=city_id)
        if "city" in result and result["city"] is None:
            return Response({"message": "city not found"}, status=status.HTTP_404_NOT_FOUND)
        if "city" in result:
            city_ser = CitySerializer(result["city"])
            state_ser = StateSerializer(result["state"])
            return Response({"city": city_ser.data, "state": state_ser.data}, status=status.HTTP_200_OK)
        # return list of cities
        city_ser = CitySerializer(result["cities"], many=True)
        return Response({"cities": city_ser.data}, status=status.HTTP_200_OK)

