"""Serializers for statistics app"""

from rest_framework import serializers

from console_api.indicator.models import Indicator
from console_api.apps.detections.models import Detection


class IndicatorSerializer(serializers.ModelSerializer):
    """Serializer for Indicator model"""

    checked_count = serializers.IntegerField()
    detected_count = serializers.IntegerField()
    type_indicator = serializers.CharField(source='type')

    class Meta:
        """Metainformation about the serializer"""

        model = Indicator
        fields = ['type_indicator', 'checked_count', 'detected_count']
        exclude = []


class DetectedIndicatorsSerializer(serializers.ModelSerializer):
    """Serializer for detected indicators"""

    class Meta:
        """Metainformation about the serializer"""

        model = Detection
        fields = ['indicator_id', "created_at"]


class IndicatorWithFeedsSerializer(serializers.ModelSerializer):
    """Serializer for Indicator model with feed"""

    class Meta:
        """Metainformation about the serializer"""

        model = Indicator
        fields = ['false_detected_counter', 'positive_detected_counter']

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('feeds')

        return queryset
