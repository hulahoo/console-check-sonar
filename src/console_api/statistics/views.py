"""Views for statistics app"""
from typing import Union
from collections import defaultdict

from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer

from console_api.constants import CREDS_ERROR
from console_api.feed.models import Feed, IndicatorFeedRelationship
from console_api.detections.models import Detection
from console_api.statistics.serializers import FeedsStatisticSerializer
from console_api.statistics.models import (
    StatCheckedObjects,
    StatMatchedObjects,
)
from console_api.statistics.services import get_objects_data_for_statistics
from console_api.services import CustomTokenAuthentication
from console_api.indicator.models import Indicator

from console_api.config.logger_config import logger


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
def indicators_statistic_view(request: Request) -> Response | JsonResponse:
    """Return JSON with detected indicators statistic"""

    if not CustomTokenAuthentication().authenticate(request):
        return Response({"detail": CREDS_ERROR}, status=HTTP_403_FORBIDDEN)

    if request.method == "GET":
        logger.info("if request.method == 'GET':")
        types_and_detections_count = defaultdict(int)

        indicators_and_types = Indicator.objects.values(
            "id", "ioc_type",
        ).annotate(tcount=Count("ioc_type")).order_by()

        for indicator in indicators_and_types:
            indicator_type = indicator["ioc_type"]
            detections_count = Detection.objects.filter(
                indicator_id=indicator["id"],
            ).count()

            types_and_detections_count[indicator_type] += detections_count

        statistic = [
            {
                "indicator-type": type_,
                "detections-count": dcount,
            }
            for type_, dcount in types_and_detections_count.items()
        ]

    return JsonResponse(statistic, safe=False)


@api_view(("GET",))
@renderer_classes((JSONRenderer,))
@require_http_methods(["GET"])
def detected_indicators_view(request: Request) -> Union[Response, JsonResponse]:
    """Return JSON with detected indicators statistic"""

    if not CustomTokenAuthentication().authenticate(request):
        return Response({"detail": CREDS_ERROR}, status=HTTP_403_FORBIDDEN)

    statistics_data = get_objects_data_for_statistics(request, Detection)

    if "error" in statistics_data.keys():
        return Response(
            {"error": statistics_data["error"]},
            HTTP_400_BAD_REQUEST,
        )

    return JsonResponse(statistics_data)


@api_view(("GET",))
@renderer_classes((JSONRenderer,))
@require_http_methods(["GET"])
def detected_objects_view(request: Request) -> Union[Response, JsonResponse]:
    """Return JSON with detected objects statistic"""

    if not CustomTokenAuthentication().authenticate(request):
        return Response({"detail": CREDS_ERROR}, status=HTTP_403_FORBIDDEN)

    statistics_data = get_objects_data_for_statistics(
        request,
        StatMatchedObjects
    )

    if "error" in statistics_data.keys():
        return Response(
            {"error": statistics_data["error"]},
            HTTP_400_BAD_REQUEST,
        )

    return JsonResponse(statistics_data)


@api_view(("GET",))
@renderer_classes((JSONRenderer,))
@require_http_methods(["GET"])
def checked_objects_view(request: Request) -> Union[Response, JsonResponse]:
    """Return JSON with checked objects statistic"""

    if not CustomTokenAuthentication().authenticate(request):
        return Response({"detail": CREDS_ERROR}, status=HTTP_403_FORBIDDEN)

    statistics_data = get_objects_data_for_statistics(
        request,
        StatCheckedObjects,
    )

    if "error" in statistics_data.keys():
        return Response(
            {"error": statistics_data["error"]},
            HTTP_400_BAD_REQUEST,
        )

    return JsonResponse(statistics_data)


@api_view(("GET",))
@require_http_methods(["GET"])
def feeds_intersection_view(request: Request) -> Response:
    if not CustomTokenAuthentication().authenticate(request):
        return Response({"detail": CREDS_ERROR}, status=HTTP_403_FORBIDDEN)

    feeds = Feed.objects.filter(is_active=True)

    indicator_ids = {}

    for feed in feeds:
        indicator_ids[feed.id] = IndicatorFeedRelationship.objects.filter(
            feed_id=feed.id
        ).values('indicator_id')

    result = []
    feed_index = 1

    for feed in feeds:
        intersections = []

        for intersection_feed in feeds:
            if not indicator_ids[feed.id]:
                # empty feed
                continue

            if intersection_feed.id == feed.id:
                # intersect with itself
                intersections.append(100)
                continue

            intersection_count = len(
                indicator_ids[feed.id].intersection(indicator_ids[intersection_feed.id])
            )

            intersections.append(round(
                intersection_count * 100 / len(indicator_ids[feed.id]), 2
            ))

        result.append({
            'feed-index': feed_index,
            'feed-name': feed.title,
            'intersections': intersections
        })

        feed_index += 1

    return Response(status=200, data=result)
