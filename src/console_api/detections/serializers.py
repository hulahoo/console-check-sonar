"""Serializers for detections app"""

from rest_framework.serializers import ModelSerializer

from console_api.detections.models import Detection


class DetectionSerializer(ModelSerializer):
    """Serializer for Detection model"""

    def to_representation(self, instance):
        """Convert representation from null to valid value"""

        data = super().to_representation(instance)

        if not data["source"]:
            data["source"] = ""

        if not data["source-message"]:
            data["source-message"] = ""

        if not data["detection-message"]:
            data["detection-message"] = ""

        if not data["tags-weight"]:
            data["tags-weight"] = 0

        if not data["indicator-weight"]:
            data["indicator-weight"] = 0

        if not data["details"]:
            data["details"] = {}

        if not data["source-event"]:
            data["source-event"] = {}

        if not data["detection-event"]:
            data["detection-event"] = {}

        return data

    class Meta:
        """Metainformation about the serializer"""

        model = Detection

        fields = [
            "id",
            "feed-names",
            "feeds",
            "feed-providers",
            "details",
            "tags",
            "tags-weight",
            "indicator-id",
            "indicator-weight",
            "source-event",
            "source",
            "source-message",
            "detection-event",
            "detection-message",
            "created-at",
        ]

        extra_kwargs = {
            "feed-names": {"source": "feeds_names"},
            "feeds": {"source": "feeds_ids"},
            "tags": {"source": "tags_ids"},
            "feed-providers": {"source": "feed_providers"},
            "tags-weight": {"source": "tags_weight"},
            "indicator-id": {"source": "indicator_id"},
            "indicator-weight": {"source": "indicator_weight"},
            "source-event": {"source": "source_event"},
            "source-message": {"source": "source_message"},
            "detection-event": {"source": "detection_event"},
            "detection-message": {"source": "detection_message"},
            "created-at": {"source": "created_at"},
        }
