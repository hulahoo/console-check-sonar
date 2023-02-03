"""Test serializers.py file"""

from django.test import TestCase
from rest_framework.serializers import ModelSerializer

from console_api.detections.models import Detection
from console_api.detections.serializers import DetectionSerializer


class AuditLogsListSerializerTests(TestCase):
    """Test AuditLogsListSerializer serializer"""

    def test_model(self) -> None:
        """Test model field of meta"""

        self.assertEqual(DetectionSerializer.Meta.model, Detection)

    def test_fields(self) -> None:
        """Test fields field of meta"""

        expected_fields = [
            "id",
            "feed-names",
            "feeds",
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

        self.assertEqual(DetectionSerializer.Meta.fields, expected_fields)

    def test_extra_kwargs(self) -> None:
        """Test extra_kwargs field of meta"""

        expected_extra_kwargs = {
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

        self.assertEqual(
            DetectionSerializer.Meta.extra_kwargs,
            expected_extra_kwargs,
        )

    def test_mro(self) -> None:
        """Test MRO"""

        self.assertIn(ModelSerializer, DetectionSerializer.mro())
