"""Serializers for detections app"""

from rest_framework import serializers

from console_api.detections.models import Detection


class DetectionSerializer(serializers.ModelSerializer):
    """Serializer for Detection model"""

    class Meta:
        """Metainformation about the serializer"""

        model = Detection

        fields = [
            "id",
            "feed-names",
            "feeds",
            "tags",
            "tags-weight",
            "indicator-id",
            "indicator-weight",
            "details",
            "source",
            "source-event",
            "source-message",
            "detection-event",
            "detection-message",
            "created-at",
        ]

        extra_kwargs = {
            "feed-names": {"source": "feeds_names"},
            "feeds": {"source": "feeds_ids"},
            "tags": {"source": "tags_ids"},
            "tags-weight": {"source": "tags_weight"},
            "indicator-id": {"source": "indicator_id"},
            "indicator-weight": {"source": "indicator_weight"},
            "source-event": {"source": "source_event"},
            "source-message": {"source": "source_message"},
            "detection-event": {"source": "detection_event"},
            "detection-message": {"source": "detection_message"},
            "created-at": {"source": "created_at"},
        }
