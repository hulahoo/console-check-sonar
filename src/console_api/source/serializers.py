"""Serializers for source app"""

from rest_framework import serializers

from console_api.source.models import Source


class SourceSerializer(serializers.ModelSerializer):
    """Serializer for Source model"""

    class Meta:
        """Metainformation about the serializer"""

        model = Source
        exclude = []
