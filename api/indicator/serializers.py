from rest_framework import serializers

from src.indicator.models import Indicator
from api.feed.serializers import DashboardFeedSerializer


class IndicatorSerializer(serializers.ModelSerializer):
    checked_count = serializers.IntegerField()
    detected_count = serializers.IntegerField()

    class Meta:
        model = Indicator
        fields = ['type', 'checked_count', 'detected_count']
        exclude = []


class CustomSerializer(serializers.ModelSerializer):
    data = IndicatorSerializer()

    class Meta:
        model = Indicator
        fields = ['data']
        exclude = []


class MatchedIndicatorSerializer(serializers.ModelSerializer):
    detected_count = serializers.IntegerField()

    class Meta:
        model = Indicator
        fields = ['last_detected_date', 'detected_count']
        exclude = []


class IndicatorWithFeedsSerializer(serializers.ModelSerializer):
    feeds = DashboardFeedSerializer(many=True, read_only=True)

    # name = serializers.CharField(feeds.name)
    # ts = django_filters.DateTimeFilter(field_name='feeds__ts', lookup_expr='iexact')
    class Meta:
        model = Indicator
        fields = ['false_detected', 'positive_detected', 'feeds']
        exclude = []

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('feeds')

        return queryset
