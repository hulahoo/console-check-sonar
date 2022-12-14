from rest_framework import serializers

from apps.indicator.models import Indicator
from api.feed.serializers import DashboardFeedSerializer


class IndicatorSerializer(serializers.ModelSerializer):
    checked_count = serializers.IntegerField()
    detected_count = serializers.IntegerField()
    type_indicator = serializers.CharField(source='type')

    class Meta:
        model = Indicator
        fields = ['type_indicator', 'checked_count', 'detected_count']
        exclude = []


class DataIndicatorSerializer(serializers.ModelSerializer):
    data = IndicatorSerializer(source='*')

    class Meta:
        model = Indicator
        fields = ['data']
        exclude = []


class MatchedIndicatorSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(source='detected_count')
    label = serializers.DateTimeField(source='last_detected_date')

    class Meta:
        model = Indicator
        fields = ['label', 'value']
        exclude = []


class IndicatorWithFeedsSerializer(serializers.ModelSerializer):
    feeds = DashboardFeedSerializer(many=True, read_only=True)

    #name = serializers.CharField(source='feeds.name')
    # ts = django_filters.DateTimeFilter(field_name='feeds__ts', lookup_expr='iexact')
    class Meta:
        model = Indicator
        fields = ['false_detected', 'positive_detected', 'feeds']
        exclude = []

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('feeds')

        return queryset


class MXyiSerializer(serializers.ModelSerializer):
    data = serializers.IntegerField(source='detected_count')
    label = serializers.DateTimeField(source='last_detected_date')

    class Meta:
        model = Indicator
        fields = ['label', 'value']
        exclude = []
