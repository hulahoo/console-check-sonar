"""Serializers for indicator app"""

from rest_framework import serializers

from console_api.indicator.models import Indicator
from console_api.search.models import History


class IndicatorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator

        fields = [
            "id",
            "value",
            "context",
            "feeds"
        ]


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = [
            'id',
            'search_type',
            'query_text',
            'query_data',
            'results',
            'created_by'
        ]
