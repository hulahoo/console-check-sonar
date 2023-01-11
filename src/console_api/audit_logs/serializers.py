"""Serializers for audit_logs app"""

from rest_framework import serializers

from console_api.audit_logs.models import AuditLogs


class AuditLogsSerializer(serializers.ModelSerializer):
    """Serializer for AuditLogs model"""

    class Meta:
        """Metainformation about the serializer"""

        model = AuditLogs

        fields = [
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

        extra_kwargs = {
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
