"""Test apps.py file"""

from django.apps import AppConfig
from django.test import TestCase

from console_api.detections.apps import DetectionsConfig
from console_api.constants import DEFAULT_AUTO_FIELD


class DetectionsConfigTests(TestCase):
    """Test DetectionsConfig class"""

    def test_default_auto_field(self) -> None:
        """Test default_auto_field field"""

        self.assertEqual(
            DetectionsConfig.default_auto_field,
            DEFAULT_AUTO_FIELD,
        )

    def test_name(self) -> None:
        """Test name field"""

        self.assertEqual(DetectionsConfig.name, "console_api.detections")

    def test_mro(self) -> None:
        """Test MRO"""

        self.assertIn(AppConfig, DetectionsConfig.mro())
