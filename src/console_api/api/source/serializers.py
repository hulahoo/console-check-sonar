from rest_framework import serializers

from apps.source.models import Source


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        exclude = []
