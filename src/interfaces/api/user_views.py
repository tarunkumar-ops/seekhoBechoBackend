from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from src.container import get_container
from src.interfaces.api.user_serializers import UserDetailsSerializer, UpdateUserSerializer
from src.application.dtos.auth_dtos import UpdateUserInput
from src.shared.exceptions import ValidationError


class UserDetailsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_id = int(request.user.id)
        out = get_container().get_user_details().execute(user_id=user_id)
        if out is None:
            return Response({"message": "not found"}, status=status.HTTP_404_NOT_FOUND)
        ser = UserDetailsSerializer(out.__dict__)
        return Response(ser.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser = UpdateUserSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        input_dto = UpdateUserInput(**ser.validated_data)
        try:
            out = get_container().update_user_details().execute(user_id=int(request.user.id), input_dto=input_dto)
        except ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        if out is None:
            return Response({"message": "not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserDetailsSerializer(out.__dict__).data, status=status.HTTP_200_OK)

