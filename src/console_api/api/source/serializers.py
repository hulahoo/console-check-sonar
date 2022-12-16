from rest_framework import serializers

from console_api.apps.source.models import Source


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        exclude = []
