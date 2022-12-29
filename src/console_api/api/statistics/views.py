"""Views for statistics app"""

from django.http import JsonResponse
from pandas import date_range
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request

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
from console_api.api.statistics.constants import PERIOD_FORMAT
from console_api.api.statistics.services import get_period_query_params


class FeedStatiscList(generics.ListAPIView):
    """FeedStatiscList"""

    pagination_class = PageNumberPagination
    serializer_class = IndicatorWithFeedsSerializer
    queryset = Indicator.objects.all().prefetch_related("feeds")


def detected_indicators_view(request: Request) -> JsonResponse:
    """Return JSON with detected indicators statistic"""

    # 1 minute by default
    frequency = request.GET.get('frequency', "T")

    start_period_at, finish_period_at = get_period_query_params(request)

    detections = Detection.objects.filter(
        created_at__range=(start_period_at, finish_period_at),
    )

    date_and_detection_amount = {
        str(date.strftime(PERIOD_FORMAT)): 0
        for date in date_range(start_period_at, finish_period_at, freq=frequency)
    }

    for detection_obj in detections:
        if frequency == "T":
            date = detection_obj.created_at.strftime(PERIOD_FORMAT)
        elif frequency == "H":
            date = start_period_at.replace(hour=detection_obj.created_at.hour)

        date_and_detection_amount[date] += 1

    return JsonResponse({
        "labels": list(date_and_detection_amount.keys()),
        "values": list(date_and_detection_amount.values()),
    })


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
