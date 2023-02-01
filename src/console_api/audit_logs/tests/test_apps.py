"""Test apps.py file"""

from django.apps import AppConfig
from django.test import TestCase

from console_api.audit_logs.apps import AuditLogsConfig
from console_api.constants import DEFAULT_AUTO_FIELD


class AuditLogsConfigTests(TestCase):
    """Test AuditLogsConfig class"""

    def test_default_auto_field(self) -> None:
        """Test default_auto_field field"""

        self.assertEqual(
            AuditLogsConfig.default_auto_field,
            DEFAULT_AUTO_FIELD,
        )

    def test_name(self) -> None:
        """Test name field"""

        self.assertEqual(AuditLogsConfig.name, "console_api.audit_logs")

    def test_mro(self) -> None:
        """Test MRO"""

        self.assertIn(AppConfig, AuditLogsConfig.mro())
