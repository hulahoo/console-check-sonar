"""Views for search app"""

from json import loads
from typing import List

from django.core import serializers
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.http import require_http_methods
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)

from console_api.constants import CREDS_ERROR, SEARCH_QUERY_ERROR
from console_api.detections.models import Detection
from console_api.indicator.models import Indicator
from console_api.search.enums import SearchStatus
from console_api.search.models import History
from console_api.services import CustomTokenAuthentication
from console_api.search.serializers import SearchHistorySerializer
from console_api.tag.models import Tag


@api_view(["GET"])
@require_http_methods(["GET"])
def search_detections_by_text_view(request: Request) -> Response:
    """Search detections by text"""

    if not CustomTokenAuthentication().authenticate(request):
        return Response({"detail": CREDS_ERROR}, status=HTTP_403_FORBIDDEN)

    user, _ = CustomTokenAuthentication().authenticate(request)

    query = request.GET.get('query')

    if not query:
        return Response(
            {"detail": SEARCH_QUERY_ERROR},
            status=HTTP_400_BAD_REQUEST,
        )

    detections = Detection.objects.filter(
        Q(source__contains=query)
        | Q(source_message__contains=query)
        | Q(detection_message__contains=query)
    )

    search_history = SearchHistorySerializer(data={
        'search_type': 'by-text',
        'query_text': query,
        'query_data': None,
        'results': serializers.serialize(
            "json",
            detections,
            fields=('id', "source", 'source_message', "detection_message"),
        ),
        'created_by': user.id,
    })

    if search_history.is_valid():
        result = search_history.save()

        return Response(status=HTTP_200_OK, data={
            'created-at': result.created_at,
            'created-by': result.created_by,
            'results': [
                {
                    'id': detect.id,
                    'source': detect.source,
                    'source-message': detect.source_message,
                    'source-event': detect.source_event,
                    'details': detect.details,
                    'indicator-id': detect.indicator_id,
                    'detection-event': detect.detection_event,
                    'detection-message': detect.detection_message,
                    'tags-weight': detect.tags_weight,
                    'indicator-weight': detect.indicator_weight,
                    'created-at': detect.created_at,
                } for detect in detections
            ]
        })


@api_view(["GET"])
@require_http_methods(["GET"])
def search_indicators_by_text_view(request: Request) -> Response:
    """Search indicators by text"""

    if not CustomTokenAuthentication().authenticate(request):
        return Response({"detail": CREDS_ERROR}, status=HTTP_403_FORBIDDEN)

    user, _ = CustomTokenAuthentication().authenticate(request)

    query = request.GET.get('query')

    if not query:
        return Response(
            {"detail": SEARCH_QUERY_ERROR},
            status=HTTP_400_BAD_REQUEST
        )

    indicators = Indicator.objects.filter(
        value__contains=query,
        deleted_at=None,
    )

    search_history = SearchHistorySerializer(data={
        'search_type': 'by-text',
        'query_text': query,
        'query_data': None,
        'results': serializers.serialize(
            "json",
            indicators,
            fields=('id', 'value'),
        ),
        'created_by': user.id,
    })

    if search_history.is_valid():
        result = search_history.save()

        return Response(status=HTTP_200_OK, data={
            'created-at': result.created_at,
            'created-by': result.created_by,
            'results': [
                {
                    'id': indicator.id,
                    'feed-name': feed.get('name'),
                    'feed-provider': feed.get('provider'),
                    'context': indicator.context,
                } for indicator in indicators for feed in indicator.feeds
            ]
        })


@api_view(["GET"])
@require_http_methods(["GET"])
def search_history_view(request: Request) -> Response:
    if not CustomTokenAuthentication().authenticate(request):
        return Response(
            {"detail": CREDS_ERROR},
            status=HTTP_403_FORBIDDEN
        )

    search_history = History.objects.all()

    return Response(status=200, data=[
        {
            'id': item.id,
            'status': SearchStatus.DETECTED if loads(item.results) else SearchStatus.NOT_DETECTED,
            'created-at': item.created_at,
            'created-by': item.created_by,
            'query': item.query_text
        } for item in search_history
    ])


class SearchTagsView(APIView):

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, *args, **kwargs) -> Response:
        query = request.GET.get('query')

        if not query:
            return Response(
                {"detail": SEARCH_QUERY_ERROR},
                status=HTTP_400_BAD_REQUEST
            )

        tags: List[Tag] = Tag.objects.filter(title__contains=query)

        search_history = SearchHistorySerializer(data={
            'search_type': 'by-title',
            'query_text': query,
            'query_data': None,
            'results': serializers.serialize(
                "json",
                tags,
                fields=('id', 'title'),
            ),
            'created_by': request.user.id,
        })

        if search_history.is_valid():
            result = search_history.save()

            return Response(status=200, data={
                'created-at': result.created_at,
                'created-by': result.created_by,
                'results': [
                    {
                        "id": tag.id,
                        "title": tag.title,
                        "weight": tag.weight,
                        "created_by": tag.created_by,
                        "created_at": tag.created_at,
                    } for tag in tags
                ]
            })
