"""Serializers for context_sources app"""

from rest_framework.serializers import ModelSerializer

from console_api.context_sources.models import ContextSources


class ContextSourcesListSerializer(ModelSerializer):
    """Serializer for context sources list"""

    class Meta:
        """Metainformation about the serializer"""

        model = ContextSources

        fields = [
            "id",
            "ioc_type",
            "source_url",
            "request_method",
            "request_headers",
            "request_body",
            "inbound_removable_prefix",
            "outbound_appendable_prefix",
            "created_at",
            "created_by",
        ]

        extra_kwargs = {
            "ioc-type": {"source": "ioc_type"},
            "source-url": {"source": "source_url"},
            "request-method": {"source": "request_method"},
            "request-headers": {"source": "request_headers"},
            "request-body": {"source": "request_body"},
            "inbound-removable-prefix": {"source": "inbound_removable_prefix"},
            "outbound-appendable-prefix": {
                "source": "outbound_appendable_prefix",
            },
            "created-at": {"source": "created_at"},
            "created-by": {"source": "created_by"},
        }
