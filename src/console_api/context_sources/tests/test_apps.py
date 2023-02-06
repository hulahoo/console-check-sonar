"""Test apps.py file"""

from django.apps import AppConfig
from django.test import TestCase

from console_api.context_sources.apps import ContextSourcesConfig
from console_api.constants import DEFAULT_AUTO_FIELD


class ContextSourcesConfigTests(TestCase):
    """Test ContextSourcesConfig class"""

    def test_default_auto_field(self) -> None:
        """Test default_auto_field field"""

        self.assertEqual(
            ContextSourcesConfig.default_auto_field,
            DEFAULT_AUTO_FIELD,
        )

    def test_name(self) -> None:
        """Test name field"""

        self.assertEqual(
            ContextSourcesConfig.name,
            "console_api.context_sources",
        )

    def test_mro(self) -> None:
        """Test MRO"""

        self.assertIn(AppConfig, ContextSourcesConfig.mro())
