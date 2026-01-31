from rest_framework import serializers


class MediaPresignRequestSerializer(serializers.Serializer):
    file_name = serializers.CharField()
    content_type = serializers.CharField()
    media_type = serializers.ChoiceField(choices=[("image", "Image"), ("video", "Video")])


class MediaPresignResponseSerializer(serializers.Serializer):
    upload_url = serializers.CharField()
    key = serializers.CharField()
    public_url = serializers.CharField()

