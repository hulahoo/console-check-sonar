from rest_framework import serializers

from src.source.models import Source


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        exclude = []
