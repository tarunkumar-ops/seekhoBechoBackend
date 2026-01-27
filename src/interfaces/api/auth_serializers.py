from rest_framework import serializers


class RequestOtpSerializer(serializers.Serializer):
    phone = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)

    def validate(self, data):
        phone = data.get("phone")
        email = data.get("email")
        if not phone and not email:
            raise serializers.ValidationError("phone or email is required")
        return data


class VerifyOtpSerializer(serializers.Serializer):
    phone = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    code = serializers.CharField()

    def validate(self, data):
        phone = data.get("phone")
        email = data.get("email")
        if not phone and not email:
            raise serializers.ValidationError("phone or email is required")
        return data

 
class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

