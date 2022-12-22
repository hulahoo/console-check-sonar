"""Serializers for detections app"""

from rest_framework import serializers

from console_api.apps.detections.models import Detection


class DetectionSerializer(serializers.ModelSerializer):
    """Serializer for Detection model"""

    class Meta:
        """Metainformation about the serializer"""

        model = Detection

        fields = [
            'id', "provider", "feed-name", "tags", "context", 'source-event',
            "ioc-id", "detection-event", "created-at",
        ]

        extra_kwargs = {
            'feed-name': {'source': 'feed_name'},
            'source-event': {'source': 'source_event'},
            'ioc-id': {'source': 'ioc_id'},
            'detection-event': {'source': 'detection_event'},
            'created-at': {'source': 'created_at'},
        }
