from rest_framework import serializers


class CreateBannerRequestSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, allow_null=True)
    media_id = serializers.UUIDField()
    placement = serializers.CharField()
    platform = serializers.ChoiceField(choices=[("android", "android"), ("ios", "ios"), ("web", "web")])
    target_type = serializers.ChoiceField(choices=[("none", "none"), ("category", "category"), ("product", "product"), ("external", "external")], default="none")
    target_value = serializers.CharField(required=False, allow_null=True)
    start_at = serializers.DateTimeField(required=False, allow_null=True)
    end_at = serializers.DateTimeField(required=False, allow_null=True)
    priority = serializers.IntegerField(required=False, default=0)
    is_active = serializers.BooleanField(required=False, default=True)


class CreateBannerResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField(allow_null=True)
    media = serializers.DictField()
    placement = serializers.CharField()
    platform = serializers.CharField()
    target_type = serializers.CharField()
    target_value = serializers.CharField(allow_null=True)
    priority = serializers.IntegerField()

