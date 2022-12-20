"""Serializers for detections app"""

from rest_framework import serializers

from apps.detections.models import Detection


class DetectionSerializer(serializers.ModelSerializer):
    """Serializer for Detection model"""

    class Meta:
        """Metainformation about the serializer"""

        model = Detection
        fields = [
            'id', 'source_event', "detection_event", "created_at"
        ]

        extra_kwargs = {
            'source-event': {'source': 'source_event'},
            'detection-event': {'source': 'detection_event'},
            'created-at': {'source': 'created_at'},
        }
