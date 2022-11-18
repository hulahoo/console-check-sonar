from rest_framework import serializers

from src.indicator.models import Indicator
from api.feed.serializers import FeedSerializer


class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        exclude = []


class IndicatorWithFeedsSerializer(serializers.ModelSerializer):
    feeds = FeedSerializer(many=True, read_only=True)

    class Meta:
        model = Indicator
        exclude = []

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('feeds')

        return queryset
