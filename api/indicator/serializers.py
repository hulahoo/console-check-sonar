from rest_framework import serializers

from src.indicator.models import Indicator
from api.feed.serializers import DashboardFeedSerializer


class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = ['type', 'detected']
        exclude = []


class IndicatorWithFeedsSerializer(serializers.ModelSerializer):
    feeds = DashboardFeedSerializer(many=True, read_only=True)

    class Meta:
        model = Indicator
        fields = ['feeds', 'id', 'false_detected', 'positive_detected']
        exclude = []

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('feeds')

        return queryset
