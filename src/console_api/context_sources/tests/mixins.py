"""Mixins for tests"""

from django.test import TestCase, Client

from console_api.context_sources.models import ContextSources
from console_api.test_utils import get_authorization_token


class ContextSourcesViewTestsMixin(TestCase):
    """Mixin for ContextSourcesView tests"""

    @classmethod
    def setUpTestData(cls) -> None:
        for i in range(cls._CONTEXT_SOURCES_COUNT):
            ContextSources.objects.create(
                ioc_type="ip",
                source_url="https://virustotal.com/api/get_ip_info?ip={value}",
                request_method=f"get {i}",
                request_headers="Authorization: Bearer MDM0MjM5NDc2MD",
                request_body="test",
                inbound_removable_prefix="data",
                outbound_appendable_prefix="virustotal",
                created_by=i,
            )

        cls.client = Client()
        cls.token = get_authorization_token(cls.client)

    def get_auth_get_response(self, url: str):
        """Return authorized GET response"""

        return self.client.get(url, HTTP_AUTHORIZATION=self.token)
