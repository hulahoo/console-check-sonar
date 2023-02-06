"""Test urls.py file"""

from rest_framework.exceptions import ErrorDetail

from console_api.context_sources.tests.constants import CONTEXT_SOURCES_URL
from console_api.test_utils import TestURLMixin


class UrlsTests(TestURLMixin):
    """Test urls"""

    def test_audit_logs_endpoint(self) -> None:
        """Test /api/context-sources endpoint"""

        self._test_url(CONTEXT_SOURCES_URL, 200, is_authorized=True)

        self._test_url(
            path=CONTEXT_SOURCES_URL,
            expected_status_code=403,
            is_authorized=False,
            data={
                "detail": ErrorDetail(
                    string="Authentication credentials were not provided.",
                    code="not_authenticated",
                ),
            },
        )
