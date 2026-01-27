from rest_framework import serializers


class StateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()


class CitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()

