"""Serializers for tag app"""

from rest_framework.serializers import ModelSerializer

from console_api.tag.models import Tag


class TagSerializer(ModelSerializer):
    """Serializer for Tag model"""

    class Meta:
        """Metainformation for the serializer"""

        model = Tag
        fields = [
            "id",
            "title",
            "weight",
            "created-at",
            "updated-at",
        ]

        extra_kwargs = {
            'created-at': {'source': 'created_at'},
            "updated-at": {'source': "updated_at"},
        }
