from console_api.apps.tag.models import Tag
from console_api.apps.feed.models import Feed
from rest_framework import serializers
from console_api.api.feed.serializers import FeedShortSerializer
from console_api.api.feed.serializers import DashboardFeedSerializer
from console_api.apps.indicator.models import Indicator, IndicatorActivities


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["title", "weight"]
        exclude = []


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ["name"]
        exclude = []


class IndicatorActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorActivities
        fields = ["type", "details", "created_at"]
        extra_kwargs = {
            "created-at": {"source": "created_at"},
        }


class IndicatorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator

        fields = [
            "id",
            "ioc-type",
            "value",
            "created-at",
            "updated-at",
            "ioc-weight",
            "tags",
            "tags-weight",
            "feed-names",
        ]

        extra_kwargs = {
            "ioc-type": {"source": "ioc_type"},
            "created-at": {"source": "created_at"},
            "updated-at": {"source": "updated_at"},
            "ioc-weight": {"source": "weight"},
            "tags": {"source": "tags_ids"},
            "tags-weight": {"source": "tags_weight"},
            "feed-names": {"source": "feeds_names"},
        }


class IndicatorDetailSerializer(serializers.ModelSerializer):
    """Serializer for IndicatorDetailView"""

    feeds = FeedShortSerializer(many=True, source="feed_set")
    activities = IndicatorActivitiesSerializer(many=True)

    class Meta:
        """Metainformation about the serializer"""

        model = Indicator

        fields = [
            "id",
            "ioc-type",
            "value",
            "context",
            "created-at",
            "updated-at",
            "ioc-weight",
            "tags",
            "tags-weight",
            "feeds",
            "activities",
        ]

        extra_kwargs = {
            "ioc-type": {"source": "ioc_type"},
            "created-at": {"source": "created_at"},
            "updated-at": {"source": "updated_at"},
            "ioc-weight": {"source": "weight"},
            "tags-weight": {"source": "tags_weight"},
        }


class IndicatorSerializer(serializers.ModelSerializer):
    tags = TagSerializer()
    feeds = FeedSerializer()

    class Meta:
        model = Indicator
        fields = [
            "id",
            "ioc_type",
            "value",
            "created_at",
            "updated_at",
            "ioc_weight",
            "tags",
            "tags_weight",
        ]


class DataIndicatorSerializer(serializers.ModelSerializer):
    data = IndicatorSerializer(source="*")

    class Meta:
        model = Indicator
        fields = ["context"]
        exclude = []


class IndicatorWithFeedsSerializer(serializers.ModelSerializer):
    feeds = DashboardFeedSerializer(many=True, read_only=True)

    class Meta:
        model = Indicator
        fields = ["false_detected_counter", "positive_detected_counter", "feeds"]
        exclude = []

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related("feeds")

        return queryset


class MatchedIndicatorSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(source="detected_count")
    label = serializers.DateTimeField(source="last_detected_date")

    class Meta:
        model = Indicator
        fields = ["label", "value"]
        exclude = []


class MXyiSerializer(serializers.ModelSerializer):
    data = serializers.IntegerField(source="detected_count")
    label = serializers.DateTimeField(source="last_detected_date")

    class Meta(MatchedIndicatorSerializer.Meta):
        ...
