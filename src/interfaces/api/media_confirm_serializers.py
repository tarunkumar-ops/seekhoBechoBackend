from rest_framework import serializers


class ConfirmMediaRequestSerializer(serializers.Serializer):
    media_type = serializers.ChoiceField(choices=[("image", "Image"), ("video", "Video")])
    media_url = serializers.URLField()
    poster_url = serializers.URLField(required=False, allow_null=True)
    width = serializers.IntegerField(required=False, allow_null=True)
    height = serializers.IntegerField(required=False, allow_null=True)
    duration = serializers.FloatField(required=False, allow_null=True)


class ConfirmMediaResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    media_type = serializers.CharField()
    media_url = serializers.URLField()
    poster_url = serializers.URLField(required=False, allow_null=True)

