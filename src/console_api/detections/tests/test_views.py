"""Test views.py file"""

import secrets

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from console_api.detections.models import Detection
from console_api.detections.serializers import DetectionSerializer
from console_api.detections.tests.constants import DETECTIONS_URL
from console_api.detections.tests.mixins import DetectionListViewTestsMixin
from console_api.detections.views import DetectionListView
from console_api.constants import (
    DIFFERENT_VALUES,
    PAGE_NUMBER,
    PAGE_SIZE,
    SORT_BY,
    WRONG_PAGE_SIZE,
)
from console_api.services import CustomTokenAuthentication


class DetectionListViewFieldsTests(DetectionListViewTestsMixin):
    """Test fields for DetectionListView"""

    _DETECTIONS_COUNT = 3

    def test_authentication_classes(self) -> None:
        """Test authentication_classes field"""

        self.assertEqual(
            DetectionListView.authentication_classes,
            [CustomTokenAuthentication],
        )

    def test_permission_classes(self) -> None:
        """Test permission_classes field"""

        self.assertEqual(
            DetectionListView.permission_classes,
            [IsAuthenticated],
        )

    def test_queryset(self) -> None:
        """Test queryset field"""

        self.assertEqual(
            [detect.id for detect in DetectionListView().get_queryset()],
            [detect.id for detect in Detection.objects.all()],
        )

    def test_serializer_class(self) -> None:
        """Test serializer_class field"""

        self.assertEqual(
            DetectionListView.serializer_class,
            DetectionSerializer,
        )

    def test_mro(self) -> None:
        """Test MRO"""

        self.assertIn(ListAPIView, DetectionListView.mro())

    def test_sort_by_params(self) -> None:
        """Test __SORT_BY_PARAMS field"""

        expected_sort_by_params = (
            "id",
            "-id",
            "source",
            "-source",
            "source_message",
            "-source_message",
            "indicator_id",
            "-indicator_id",
            "detection_message",
            "-detection_message",
            "tags_weight",
            "-tags_weight",
            "indicator_weight",
            "-indicator_weight",
            "created_at",
            "-created_at",
        )

        self.assertEqual(
            DetectionListView()._SORT_BY_PARAMS,
            expected_sort_by_params,
        )
