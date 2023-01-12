"""Serializers for statistics app"""

from rest_framework.serializers import (
    CharField,
    IntegerField,
    ModelSerializer,
    SerializerMethodField,
)

from console_api.detections.models import Detection, DetectionFeedRelationship
from console_api.feed.models import Feed
from console_api.indicator.models import Indicator, IndicatorFeedRelationship


class IndicatorSerializer(ModelSerializer):
    """Serializer for Indicator model"""

    checked_count = IntegerField()
    detected_count = IntegerField()
    type_indicator = CharField(source="type")

    class Meta:
        """Metainformation for the serializer"""

        model = Indicator
        fields = ["type_indicator", "checked_count", "detected_count"]
        exclude = []


class DetectedIndicatorsSerializer(ModelSerializer):
    """Serializer for detected indicators"""

    class Meta:
        """Metainformation for the serializer"""

        model = Detection
        fields = ["indicator_id", "created_at"]


class FeedsStatisticSerializer(ModelSerializer):
    """Serializer for feeds statistic"""

    false_positive_count = SerializerMethodField("get_false_positive_count")
    detections_count = SerializerMethodField("get_detections_count")

    def get_false_positive_count(self, feed: Feed) -> int:
        """Return count of false positive indicators for the feed"""

        indicators_ids = [
            relationship.indicator_id
            for relationship in IndicatorFeedRelationship.objects.filter(
                feed_id=feed.id,
            )
        ]

        indicators = [Indicator.objects.get(id=id_) for id_ in indicators_ids]

        return len([ind for ind in indicators if ind.is_false_positive])

    def get_detections_count(self, feed: Feed) -> int:
        """Return count of feed's detections"""

        return DetectionFeedRelationship.objects.filter(
            feed_id=feed.id
        ).count()

    class Meta:
        """Metainformation for the serializer"""

        model = Feed

        fields = [
            "feed-name",
            "updated-at",
            "indicators-count",
            "false_positive_count",
            "detections_count",
        ]

        extra_kwargs = {
            "feed-name": {"source": "title"},
            "updated-at": {"source": "updated_at"},
            "indicators-count": {"source": "indicators_count"},
        }
