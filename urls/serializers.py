from rest_framework import serializers
from django.utils import timezone

class CreateShortURLSerializer(serializers.Serializer):
    long_url = serializers.URLField()
    custom_alias = serializers.CharField(required=False, max_length=32)
    expiration_date = serializers.DateTimeField(required=False)

    def validate_expiration_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Expiration date must be in the future")
        return value
