"""Test serializers.py file"""

from django.test import TestCase

from console_api.audit_logs.models import AuditLogs
from console_api.audit_logs.serializers import AuditLogsListSerializer


class AuditLogsListSerializerTests(TestCase):
    """Test AuditLogsListSerializer serializer"""

    def test_model(self) -> None:
        """Test model"""

        self.assertEqual(AuditLogsListSerializer.Meta.model, AuditLogs)

    def test_fields(self) -> None:
        """Test fields"""

        expected_fields = [
            "id",
            "service-name",
            "user-id",
            "user-name",
            "event-type",
            "object-type",
            "object-name",
            "description",
            "prev-value",
            "new-value",
            "context",
            "created-at",
        ]

        self.assertEqual(AuditLogsListSerializer.Meta.fields, expected_fields)

    def test_extra_kwargs(self) -> None:
        """Test extra_kwargs"""

        expected_extra_kwargs = {
            "service-name": {"source": "service_name"},
            "user-id": {"source": "user_id"},
            "user-name": {"source": "user_name"},
            "event-type": {"source": "event_type"},
            "object-type": {"source": "object_type"},
            "object-name": {"source": "object_name"},
            "prev-value": {"source": "prev_value"},
            "new-value": {"source": "new_value"},
            "created-at": {"source": "created_at"},
        }

        self.assertEqual(
            AuditLogsListSerializer.Meta.extra_kwargs,
            expected_extra_kwargs,
        )
