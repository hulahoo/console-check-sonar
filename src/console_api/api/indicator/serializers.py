from api.feed.serializers import DashboardFeedSerializer
from apps.indicator.models import Indicator, IndicatorActivities
from rest_framework import serializers

from apps.indicator.models import Indicator
from apps.tag.models import Tag
from apps.feed.models import Feed


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['title', 'weight']
        exclude = []


class FeedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feed
        fields = ['name']
        exclude = []

from api.feed.serializers import FeedShortSerializer


class IndicatorActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorActivities
        fields = ['type', 'details', 'created_at']


class IndicatorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator

        fields = [
            'id', 'ioc-type', 'value',
            'created-at', 'updated-at',
            'ioc-weight',
            'tags', "tags-weight",
            "feed-names"
        ]

        extra_kwargs = {
            'ioc-type': {'source': 'ioc_type'},
            'created-at': {'source': 'created_at'},
            'updated-at': {'source': 'updated_at'},
            'ioc-weight': {'source': 'weight'},
            'tags-weight': {'source': 'tags_weight'},
            'feed-names': {'source': 'feeds'},
        }


class IndicatorDetailSerializer(serializers.ModelSerializer):
    feeds = FeedShortSerializer(many=True, source='feed_set')
    activities = IndicatorActivitiesSerializer(many=True)

    class Meta:
        model = Indicator
        fields = ['uuid', 'type', 'value', 'created_at', 'updated_at', 'weight', 'tag', 'feeds', 'activities']


class IndicatorSerializer(serializers.ModelSerializer):
    tags = TagSerializer()
    feeds = FeedSerializer()

    class Meta:
        model = Indicator
        fields = [
            'id', 'ioc_type', 'value',
            'created_at', 'updated_at',
            'weight', 'tags', 'tags_weight',
        ]


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

    # name = serializers.CharField(source='feeds.name')
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
