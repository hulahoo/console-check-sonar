"""Serializers for files app"""

from rest_framework.serializers import ModelSerializer

from console_api.files.models import Files


class FileUploadSerializer(ModelSerializer):
    """Serializer for Files model"""

    class Meta:
        """Metainformation about the serializer"""

        model = Files

        fields = [
            "id",
            "bucket",
            "key",
            "content",
            "created_at",
            "created_by",
        ]
