"""Views for statistics app"""

from collections import defaultdict
from requests import get
from typing import Union

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework.generics import RetrieveAPIView
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer

from console_api.constants import CREDS_ERROR
from console_api.detections.models import Detection
from console_api.feed.models import Feed, IndicatorFeedRelationship
from console_api.indicator.models import Indicator
from console_api.statistics.serializers import FeedsStatisticSerializer
from console_api.statistics.models import (
    StatCheckedObjects,
    StatMatchedObjects,
)
from console_api.statistics.services import (
    get_objects_data_for_statistics,
    get_indicators_statistic,
)
from console_api.services import CustomTokenAuthentication
from console_api.mixins import get_boolean_from_str


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

    result = get_indicators_statistic()

    return JsonResponse(result, safe=False)


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
            {"detail": statistics_data["error"]},
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

    statistics_data = get_objects_data_for_statistics(request, StatMatchedObjects)

    if "error" in statistics_data.keys():
        return Response(
            {"detail": statistics_data["error"]},
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
            {"detail": statistics_data["error"]},
            HTTP_400_BAD_REQUEST,
        )

    return JsonResponse(statistics_data)


class FeedsIntersectionView(RetrieveAPIView):
    """View with feeds intersection"""

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def __get_relevant_indicators(self, request) -> tuple:
        """Return indicators relevants to the request params"""

        is_false_positive = request.GET.get("enable-false-positive", "false")
        is_false_positive = get_boolean_from_str(is_false_positive)

        return tuple(
            indicator.get("id")
            for indicator in Indicator.objects.filter(
                is_false_positive=is_false_positive,
            ).values("id")
        )

    def __get_relevant_feeds_and_indicators_ids(
            self, feeds, relevant_indicators) -> dict:
        """Return feeds and indicators ids relevant to the request"""

        feeds_and_indicators_ids = {
            feed.id: IndicatorFeedRelationship.objects.filter(
                feed_id=feed.id,
            ).values("indicator_id")
            for feed in feeds
        }

        relevant_feeds_and_indicators_ids = defaultdict(list)

        for feed_id, indicators_ids in feeds_and_indicators_ids.items():
            relevant_indicators_ids = {
                indicator.get("indicator_id")
                for indicator in indicators_ids
                if indicator.get("indicator_id") in relevant_indicators
            }

            relevant_feeds_and_indicators_ids[feed_id] = relevant_indicators_ids

        return dict(relevant_feeds_and_indicators_ids)

    def get(self, request: Request, *args, **kwargs) -> Response:
        """Return feeds intersection"""

        if not CustomTokenAuthentication().authenticate(request):
            return Response({"detail": CREDS_ERROR}, status=HTTP_403_FORBIDDEN)

        relevant_indicators = self.__get_relevant_indicators(request)
        active_feeds = Feed.objects.filter(is_active=True)

        feeds_and_indicators_ids = self.__get_relevant_feeds_and_indicators_ids(
            active_feeds, relevant_indicators
        )

        result = []

        for feed_index, feed in enumerate(active_feeds, start=1):
            intersections = []

            for intersection_feed in active_feeds:
                if not feeds_and_indicators_ids[feed.id]:
                    # empty feed
                    continue

                if intersection_feed.id == feed.id:
                    # intersect with itself
                    intersections.append(100)
                    continue

                intersection_count = len(
                    feeds_and_indicators_ids[feed.id].intersection(
                        feeds_and_indicators_ids[intersection_feed.id]
                    )
                )

                intersections.append(
                    round(
                        intersection_count
                        * 100
                        / len(feeds_and_indicators_ids[feed.id]),
                        2,
                    )
                )

            result.append(
                {
                    "feed-index": feed_index,
                    "feed-name": feed.title,
                    "intersections": intersections,
                }
            )

        return Response(status=HTTP_200_OK, data=result)


class FeedForceUpdateStatistics(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, *args, **kwargs) -> Response:
        feeds_update_statistics = (
            f"{settings.FEEDS_IMPORTING_SERVICE_URL}/api/force-update/statistics"
        )
        try:
            response = get(feeds_update_statistics)
        except Exception as error:
            return Response(
                {"detail": str(error)}, status=HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(response, status=HTTP_200_OK)
