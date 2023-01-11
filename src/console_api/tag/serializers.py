"""Serializers for tag app"""

from rest_framework import serializers

from console_api.tag.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model"""

    class Meta:
        """Metainformation for the model"""

        model = Tag
        exclude = []
