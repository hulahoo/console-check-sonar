"""Serializers for statistics app"""

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)

from console_api.detections.models import Detection, DetectionFeedRelationship
from console_api.feed.models import Feed
from console_api.indicator.models import Indicator, IndicatorFeedRelationship

from console_api.config.logger_config import logger


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

        logger.info("def get_false_positive_count(self, feed: Feed) -> int:")

        indicators_ids = [
            relationship.indicator_id
            for relationship in IndicatorFeedRelationship.objects.filter(
                feed_id=feed.id,
            )
        ]

        logger.info("indicators_ids = [relationship.indicator_id]")

        indicators = [Indicator.objects.get(id=id_) for id_ in indicators_ids]
        logger.info("indicators = [Indicator.objects.get(id=id_) for id_ in indicators_ids]")

        return len([ind for ind in indicators if ind.is_false_positive])

    def get_detections_count(self, feed: Feed) -> int:
        """Return count of feed's detections"""

        logger.info("def get_detections_count(self, feed: Feed) -> int:")

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
