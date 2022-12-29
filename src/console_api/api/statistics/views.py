"""Views for statistics app"""

from django.http import JsonResponse
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request

from console_api.apps.feed.models import Feed
from console_api.apps.indicator.models import Indicator
from console_api.apps.detections.models import Detection
from console_api.api.statistics.serializers import (
    DetectedIndicatorsSerializer,
    IndicatorWithFeedsSerializer,
)
from console_api.apps.statistics.models import (
    StatCheckedObjects,
    StatMatchedObjects,
)
from console_api.api.statistics.services import get_objects_data_for_statistics


class FeedStatiscList(generics.ListAPIView):
    """FeedStatiscList"""

    pagination_class = PageNumberPagination
    serializer_class = IndicatorWithFeedsSerializer
    queryset = Indicator.objects.all().prefetch_related("feeds")


def detected_indicators_view(request: Request) -> JsonResponse:
    """Return JSON with detected indicators statistic"""

    statistics_data = get_objects_data_for_statistics(request, Detection)

    return JsonResponse(statistics_data)


def detected_objects_view(request: Request) -> JsonResponse:
    """Return JSON with detected objects statistic"""

    statistics_data = get_objects_data_for_statistics(
        request,
        StatMatchedObjects
    )

    return JsonResponse(statistics_data)


def checked_objects_view(request: Request) -> JsonResponse:
    """Return JSON with checked objects statistic"""

    statistics_data = get_objects_data_for_statistics(
        request,
        StatCheckedObjects,
    )

    return JsonResponse(statistics_data)


class FeedsIntersectionList(generics.ListAPIView):
    """FeedsIntersectionList"""

    serializer_class = DetectedIndicatorsSerializer
    model = Feed

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return JsonResponse({"data": queryset})
