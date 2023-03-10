"""Services for search app"""

from django.core import serializers
from django.db.models import Q
from django.db.models.query import QuerySet
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)

from console_api.constants import CREDS_ERROR, SEARCH_QUERY_ERROR
from console_api.detections.models import Detection
from console_api.indicator.models import Indicator
from console_api.search.serializers import SearchHistorySerializer
from console_api.users.models import User


def get_search_history(
        query: str, objects: QuerySet,
        fields: tuple, created_by: int) -> SearchHistorySerializer:
    """Return search history for the search query"""

    return SearchHistorySerializer(
        data={
            "search_type": "by-text",
            "query_text": query,
            "query_data": None,
            "results": serializers.serialize("json", objects, fields=fields),
            "created_by": created_by,
        }
    )


def get_detections_by_query(query: str) -> QuerySet:
    """Return detections found by query"""

    detections = list(Detection.objects.filter(
        Q(source__icontains=query)
        | Q(detection_message__icontains=query)
        | Q(source_message__icontains=query)
        | Q(source_event__icontains=query)
        | Q(detection_event__icontains=query)
    ))

    detections_2 = [
        detect for detect in Detection.objects.all()
        if query in detect.feeds_names
    ]

    detections.extend(detections_2)

    return detections


def get_indicators_by_query(query_type: str, values: list) -> QuerySet:
    """Return indicators found by query"""

    indicators = Indicator.objects.filter(value__icontains=values[0])

    for val in values[1:]:
        indicators |= Indicator.objects.filter(value__icontains=val)

    if query_type == "hashes":
        indicators = indicators.filter(ioc_type="hash")

    return indicators


def get_detections_search_results(detections: QuerySet) -> tuple:
    """Return search detections results"""

    return (
        {
            "id": detect.id,
            "source": detect.source or "",
            "source-message": detect.source_message or "",
            "source-event": detect.source_event or {},
            "details": detect.details or {},
            "indicator-id": detect.indicator_id,
            "detection-event": detect.detection_event or {},
            "detection-message": detect.detection_message or {},
            "tags-weight": detect.tags_weight or 0,
            "indicator-weight": detect.indicator_weight or 0,
            "created-at": detect.created_at,
        }
        for detect in detections
    )


def get_indicators_search_results(indicators: QuerySet) -> tuple:
    """Return search indicators results"""

    return tuple(
        {
            "id": indicator.id,
            "feed-name": feed.get("name"),
            "feed-provider": feed.get("provider"),
            "context": indicator.context or {},
        }
        for indicator in indicators
        for feed in indicator.get_feeds(is_all=True)
    )


def get_creds_error_response() -> Response:
    """Return response with credentials error"""

    return Response({"detail": CREDS_ERROR}, status=HTTP_403_FORBIDDEN)


def get_search_query_error_response() -> Response:
    """Return response with search query error"""

    return Response(
        {"detail": SEARCH_QUERY_ERROR},
        status=HTTP_400_BAD_REQUEST,
    )


def get_search_results_response(
        search_history: SearchHistorySerializer,
        search_results: QuerySet) -> Response:
    """Return response with search results"""

    if not search_history.is_valid():
        return Response(search_history.errors, status=HTTP_400_BAD_REQUEST)

    result = search_history.save()

    return Response(
        status=HTTP_200_OK,
        data={
            "created-at": result.created_at,
            "created-by": {
                "id": result.created_by,
                "login": User.objects.get(id=result.created_by).login,
            },
            "results": search_results,
        },
    )
