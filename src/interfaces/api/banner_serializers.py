from rest_framework import serializers


class MediaSerializer(serializers.Serializer):
    id = serializers.CharField()
    media_type = serializers.CharField()
    media_url = serializers.URLField()
    poster_url = serializers.URLField(allow_null=True, required=False)
    width = serializers.IntegerField(allow_null=True, required=False)
    height = serializers.IntegerField(allow_null=True, required=False)
    duration = serializers.FloatField(allow_null=True, required=False)


class BannerSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField(allow_null=True, required=False)
    media = MediaSerializer()
    placement = serializers.CharField()
    platform = serializers.CharField()
    target_type = serializers.CharField()
    target_value = serializers.CharField(allow_null=True, required=False)
    priority = serializers.IntegerField()

