"""Serializers for indicator app"""

from rest_framework import serializers

from console_api.search.models import History


class SearchHistorySerializer(serializers.ModelSerializer):
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
