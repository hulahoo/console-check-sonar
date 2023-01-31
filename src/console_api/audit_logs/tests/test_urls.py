"""Test urls.py file"""

from console_api.audit_logs.tests.constants import AUDIT_LOGS_URL
from console_api.test_utils import TestURLMixin

from rest_framework.exceptions import ErrorDetail


class UrlsTests(TestURLMixin):
    """Test urls"""

    def test_index(self) -> None:
        """Test /api/audit-logs path"""

        self._test_url(AUDIT_LOGS_URL, 200, is_authorized=True)

        self._test_url(
            path=AUDIT_LOGS_URL,
            expected_status_code=403,
            is_authorized=False,
            data={
                'detail': ErrorDetail(
                    string='Authentication credentials were not provided.',
                    code='not_authenticated'
                )
            }
        )
