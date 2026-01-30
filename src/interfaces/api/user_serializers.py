from rest_framework import serializers
from src.interfaces.api.config_serializers import InterestedPlatformSerializer


class UserDetailsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_code = serializers.CharField(required=False, allow_null=True)
    full_name = serializers.CharField(required=False, allow_null=True)
    whatsapp_number = serializers.CharField(required=False, allow_null=True)
    email = serializers.EmailField(required=False, allow_null=True)
    country_id = serializers.IntegerField(required=False, allow_null=True)
    state_id = serializers.IntegerField(required=False, allow_null=True)
    city_id = serializers.IntegerField(required=False, allow_null=True)
    occupation_id = serializers.IntegerField(required=False, allow_null=True)
    language_id = serializers.IntegerField(required=False, allow_null=True)
    country_name = serializers.CharField(required=False, allow_null=True)
    state_name = serializers.CharField(required=False, allow_null=True)
    city_name = serializers.CharField(required=False, allow_null=True)
    occupation_name = serializers.CharField(required=False, allow_null=True)
    language_name = serializers.CharField(required=False, allow_null=True)
    budget_to_invest = serializers.CharField(required=False, allow_null=True)
    gender = serializers.CharField(required=False, allow_null=True)
    status = serializers.BooleanField(required=False, allow_null=True)
    interested_platforms = InterestedPlatformSerializer(many=True, required=False)


class UpdateUserSerializer(serializers.Serializer):
    # Make fields mandatory as requested
    full_name = serializers.CharField(required=True, allow_null=False)
    city_id = serializers.IntegerField(required=True, allow_null=False)
    state_id = serializers.IntegerField(required=True, allow_null=False)
    whatsapp_number = serializers.CharField(required=True, allow_null=False)
    email = serializers.EmailField(required=True, allow_null=False)
    platform_ids = serializers.ListField(child=serializers.IntegerField(), required=True, allow_empty=False)
    budget_to_invest = serializers.CharField(required=True, allow_null=False)
    gender = serializers.CharField(required=True, allow_null=False)
    occupation_id = serializers.IntegerField(required=True, allow_null=False)
    # Optional/derived fields
    language_id = serializers.IntegerField(required=False, allow_null=True)

