from rest_framework import serializers


class RequestOtpSerializer(serializers.Serializer):
    phone = serializers.CharField()


class VerifyOtpSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()

