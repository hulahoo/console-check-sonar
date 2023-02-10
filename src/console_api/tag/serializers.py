"""Serializers for tag app"""

from rest_framework.serializers import ModelSerializer

from console_api.tag.models import Tag


class TagsListSerializer(ModelSerializer):
    """Serializer for tags list"""

    def to_representation(self, instance):
        """Convert representation from null to valid value"""

        data = super().to_representation(instance)

        if not data["updated-at"]:
            data["updated-at"] = data["created-at"]

        if not data["weight"]:
            data["weight"] = 0

        return data

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


class TagCreateSerializer(ModelSerializer):
    """Serializer for tag creation"""

    class Meta:
        """Metainformation for the serializer"""

        model = Tag
        fields = [
            "id",
            "title",
            "weight",
        ]
