"""Serializers for indicator app"""

from json import loads

from rest_framework.serializers import ModelSerializer

from console_api.search.models import History
from console_api.users.models import User


class SearchHistorySerializer(ModelSerializer):
    """Serializer for History model"""

    class Meta:
        """Metainformation about the serializer"""

        model = History

        fields = [
            "id",
            "search_type",
            "query_text",
            "query_data",
            "results",
            "created_by",
        ]


class SearchHistoryListSerializer(ModelSerializer):
    """Serializer for History objects list"""

    def to_representation(self, instance):
        """Convert representation from null to valid value"""

        data = super().to_representation(instance)

        status = data["status"]
        created_by = data["created-by"]

        data["status"] = "detected" if loads(status) else "not-detected"
        data["created-by"] = {
            "id": created_by,
            "login": User.objects.get(id=created_by).login,
        }

        return data

    class Meta:
        """Metainformation about the serializer"""

        model = History

        fields = [
            "id",
            "status",
            "created-at",
            "created-by",
            "query",
        ]

        extra_kwargs = {
            "status": {"source": "results"},
            "created-at": {"source": "created_at"},
            "created-by": {"source": "created_by"},
            "query": {"source": "query_text"},
        }
