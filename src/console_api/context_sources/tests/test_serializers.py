"""Test serializers.py file"""

from django.test import TestCase
from rest_framework.serializers import ModelSerializer

from console_api.context_sources.models import ContextSources
from console_api.context_sources.serializers import ContextSourcesListSerializer


class ContextSourcesListSerializerTests(TestCase):
    """Test ContextSourcesListSerializer serializer"""

    def test_model(self) -> None:
        """Test model field of meta"""

        self.assertEqual(
            ContextSourcesListSerializer.Meta.model,
            ContextSources,
        )

    def test_fields(self) -> None:
        """Test fields field of meta"""

        expected_fields = [
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

        self.assertEqual(
            ContextSourcesListSerializer.Meta.fields,
            expected_fields,
        )

    def test_extra_kwargs(self) -> None:
        """Test extra_kwargs field of meta"""

        expected_extra_kwargs = {
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

        self.assertEqual(
            ContextSourcesListSerializer.Meta.extra_kwargs,
            expected_extra_kwargs,
        )

    def test_mro(self) -> None:
        """Test MRO"""

        self.assertIn(ModelSerializer, ContextSourcesListSerializer.mro())
