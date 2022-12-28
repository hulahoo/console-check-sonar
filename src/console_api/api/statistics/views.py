"""Views for statistics app"""

from django.http import JsonResponse
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from console_api.apps.feed.models import Feed
from console_api.apps.indicator.models import Indicator
from console_api.apps.detections.models import Detection
from console_api.api.statistics.serializers import (
    CheckedObjectsSerializer,
    DetectedIndicatorsSerializer,
    DetectedObjectsSerializer,
    IndicatorWithFeedsSerializer,
)
from console_api.apps.statistics.models import (
    StatCheckedObjects,
    StatMatchedObjects,
)


class FeedStatiscList(generics.ListAPIView):
    """FeedStatiscList"""

    pagination_class = PageNumberPagination
    serializer_class = IndicatorWithFeedsSerializer
    queryset = Indicator.objects.all().prefetch_related("feeds")


class DetectedIndicatorsView(generics.ListAPIView):
    """Detected indicators"""

    serializer_class = DetectedIndicatorsSerializer

    def get_queryset(self):
        start_period_at = self.request.GET.get('start-period-at')
        finish_period_at = self.request.GET.get('finish-period-at')

        detections = Detection.objects.filter(
            created_at__range=(start_period_at, finish_period_at),
        )

        return detections.values("indicator_id", "created_at")


class DetectedObjectsView(generics.ListAPIView):
    """Detected objects"""

    serializer_class = DetectedObjectsSerializer

    def get_queryset(self):
        start_period_at = self.request.GET.get('start-period-at')
        finish_period_at = self.request.GET.get('finish-period-at')

        objects = StatMatchedObjects.objects.filter(
            created_at__range=(start_period_at, finish_period_at),
        )

        return objects.values("indicator_id", "created_at")
# Раз в день

class CheckedObjectsView(generics.ListAPIView):
    """Detected objects"""

    serializer_class = CheckedObjectsSerializer

    def get_queryset(self):
        start_period_at = self.request.GET.get('start-period-at')
        finish_period_at = self.request.GET.get('finish-period-at')

        objects = StatCheckedObjects.objects.filter(
            created_at__range=(start_period_at, finish_period_at),
        )

        return objects.values("id", "created_at")


class FeedsIntersectionList(generics.ListAPIView):
    """FeedsIntersectionList"""

    serializer_class = DetectedIndicatorsSerializer
    model = Feed

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return JsonResponse({"data": queryset})
