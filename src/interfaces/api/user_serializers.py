from rest_framework import serializers


class UserDetailsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_code = serializers.CharField(required=False, allow_null=True)
    full_name = serializers.CharField(required=False, allow_null=True)
    whatsapp_number = serializers.CharField(required=False, allow_null=True)
    email = serializers.EmailField(required=False, allow_null=True)
    country_id = serializers.IntegerField(required=False, allow_null=True)
    state_id = serializers.IntegerField(required=False, allow_null=True)
    city_id = serializers.IntegerField(required=False, allow_null=True)
    platform_id = serializers.IntegerField(required=False, allow_null=True)
    occupation_id = serializers.IntegerField(required=False, allow_null=True)
    language_id = serializers.IntegerField(required=False, allow_null=True)
    country_name = serializers.CharField(required=False, allow_null=True)
    state_name = serializers.CharField(required=False, allow_null=True)
    city_name = serializers.CharField(required=False, allow_null=True)
    platform_name = serializers.CharField(required=False, allow_null=True)
    occupation_name = serializers.CharField(required=False, allow_null=True)
    language_name = serializers.CharField(required=False, allow_null=True)
    budget_to_invest = serializers.CharField(required=False, allow_null=True)
    gender = serializers.CharField(required=False, allow_null=True)
    status = serializers.BooleanField(required=False, allow_null=True)


class UpdateUserSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=False, allow_null=True)
    email = serializers.EmailField(required=False, allow_null=True)
    whatsapp_number = serializers.CharField(required=False, allow_null=True)
    country_id = serializers.IntegerField(required=False, allow_null=True)
    state_id = serializers.IntegerField(required=False, allow_null=True)
    city_id = serializers.IntegerField(required=False, allow_null=True)
    platform_id = serializers.IntegerField(required=False, allow_null=True)
    occupation_id = serializers.IntegerField(required=False, allow_null=True)
    language_id = serializers.IntegerField(required=False, allow_null=True)
    budget_to_invest = serializers.CharField(required=False, allow_null=True)
    gender = serializers.CharField(required=False, allow_null=True)

