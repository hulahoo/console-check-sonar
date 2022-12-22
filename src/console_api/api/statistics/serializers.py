"""Serializers for statistics app"""

from rest_framework import serializers

from console_api.apps.indicator.models import Indicator


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


class DataIndicatorSerializer(serializers.ModelSerializer):
    """Serializer for Indicator model with data"""

    data = IndicatorSerializer(source='*')

    class Meta:
        """Metainformation about the serializer"""

        model = Indicator
        fields = ['data']
        exclude = []


class MatchedIndicatorSerializer(serializers.ModelSerializer):
    """Serializer for Indicator model with values"""

    values = serializers.IntegerField(source='value')

    class Meta:
        """Metainformation about the serializer"""

        model = Indicator
        fields = ['values']
        exclude = []


class IndicatorWithFeedsSerializer(serializers.ModelSerializer):
    """Serializer for Indicator model with feed"""

    class Meta:
        """Metainformation about the serializer"""

        model = Indicator
        fields = ['false_detected_counter', 'positive_detected_counter']
        exclude = []

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('feeds')

        return queryset


class MXyiSerializer(serializers.ModelSerializer):
    """Serializer for Indicator model with data and lable"""

    data = serializers.IntegerField(source='detected_count')
    label = serializers.DateTimeField(source='last_detected_date')

    class Meta:
        """Metainformation about the serializer"""

        model = Indicator
        fields = ['label', 'value']
        exclude = []
