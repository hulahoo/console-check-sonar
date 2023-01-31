"""Test urls.py file"""

from console_api.audit_logs.tests.constants import AUDIT_LOGS_URL
from console_api.test_utils import TestURLMixin


class UrlsTests(TestURLMixin):
    """Test urls"""

    def test_index(self) -> None:
        """Test /api/audit-logs path"""

        self._test_url(AUDIT_LOGS_URL, 200, is_authorized=True)
        self._test_url(AUDIT_LOGS_URL, 403, is_authorized=False)
