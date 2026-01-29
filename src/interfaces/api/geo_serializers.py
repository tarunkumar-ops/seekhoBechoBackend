from rest_framework import serializers


class StateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()


class CitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    state_id = serializers.IntegerField(required=False, allow_null=True)
    state_title = serializers.CharField(required=False, allow_null=True)

