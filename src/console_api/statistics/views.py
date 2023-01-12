"""Views for statistics app"""

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer

from console_api.feed.models import Feed
from console_api.detections.models import Detection
from console_api.statistics.serializers import (
    DetectedIndicatorsSerializer,
    FeedsStatisticSerializer,
)
from console_api.statistics.models import (
    StatCheckedObjects,
    StatMatchedObjects,
)
from console_api.statistics.services import get_objects_data_for_statistics
from console_api.services import CustomTokenAuthentication


class FeedsStatisticView(generics.ListAPIView):
    """Statistics for feeds"""

    pagination_class = PageNumberPagination
    serializer_class = FeedsStatisticSerializer
    queryset = Feed.objects.all()

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]


@api_view(("GET",))
@renderer_classes((JSONRenderer,))
@require_http_methods(["GET"])
def detected_indicators_view(request: Request) -> JsonResponse:
    """Return JSON with detected indicators statistic"""

    if not CustomTokenAuthentication().authenticate(request):
        return Response(status=HTTP_403_FORBIDDEN)

    statistics_data = get_objects_data_for_statistics(request, Detection)

    return JsonResponse(statistics_data)


@api_view(("GET",))
@renderer_classes((JSONRenderer,))
@require_http_methods(["GET"])
def detected_objects_view(request: Request) -> JsonResponse:
    """Return JSON with detected objects statistic"""

    if not CustomTokenAuthentication().authenticate(request):
        return Response(status=HTTP_403_FORBIDDEN)

    statistics_data = get_objects_data_for_statistics(
        request,
        StatMatchedObjects
    )

    return JsonResponse(statistics_data)


@api_view(("GET",))
@renderer_classes((JSONRenderer,))
@require_http_methods(["GET"])
def checked_objects_view(request: Request) -> JsonResponse:
    """Return JSON with checked objects statistic"""

    if not CustomTokenAuthentication().authenticate(request):
        return Response(status=HTTP_403_FORBIDDEN)

    statistics_data = get_objects_data_for_statistics(
        request,
        StatCheckedObjects,
    )

    return JsonResponse(statistics_data)


class FeedsIntersectionList(generics.ListAPIView):
    """FeedsIntersectionList"""

    serializer_class = DetectedIndicatorsSerializer
    model = Feed
    queryset = Feed.objects.all()

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return JsonResponse({"data": queryset})
