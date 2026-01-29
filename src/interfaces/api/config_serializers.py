from rest_framework import serializers


class OccupationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()


class InterestedPlatformSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()

