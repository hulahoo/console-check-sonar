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
from console_api.detections.models import Detection, DetectionFeedRelationship
from console_api.indicator.models import Indicator
from console_api.search.serializers import SearchHistorySerializer
from console_api.users.models import User
from console_api.feed.models import Feed


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

    return Detection.objects.filter(
        Q(source__contains=query)
        | Q(source_message__contains=query)
        | Q(detection_message__contains=query)
    )


def get_indicators_by_query(query: str) -> QuerySet:
    """Return indicators found by query"""

    return Indicator.objects.filter(
        value__contains=query,
        deleted_at=None,
    )


def get_detections_search_results(detections: QuerySet) -> tuple:
    """Return search detections results"""

    return (
        {
            "id": detect.id,
            "source": detect.source,
            "source-message": detect.source_message,
            "source-event": detect.source_event,
            "details": detect.details,
            "indicator-id": detect.indicator_id,
            "detection-event": detect.detection_event,
            "detection-message": detect.detection_message,
            "tags-weight": detect.tags_weight,
            "indicator-weight": detect.indicator_weight,
            "created-at": detect.created_at,
        }
        for detect in detections
    )


def get_indicators_search_results(indicators: QuerySet) -> tuple:
    """Return search indicators results"""

    return (
        {
            "id": indicator.id,
            "feed-name": feed.get("name"),
            "feed-provider": feed.get("provider"),
            "context": indicator.context,
        }
        for indicator in indicators
        for feed in indicator.feeds
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
