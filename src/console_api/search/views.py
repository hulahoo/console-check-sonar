"""Views for search app"""

from json import loads
from typing import List

from django.core import serializers
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.http import require_http_methods
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)

from console_api.tag.models import Tag
from console_api.search.enums import SearchStatus
from console_api.search.models import History, Indicator
from console_api.services import CustomTokenAuthentication
from console_api.search.serializers import SearchHistorySerializer
from console_api.constants import CREDS_ERROR, SEARCH_QUERY_ERROR


@api_view(["GET"])
@require_http_methods(["GET"])
def search_by_text_view(request: Request) -> Response:
    if not CustomTokenAuthentication().authenticate(request):
        return Response({"detail": CREDS_ERROR}, status=HTTP_403_FORBIDDEN)

    user, _ = CustomTokenAuthentication().authenticate(request)

    query = request.GET.get('query')

    if not query:
        return Response(
            {"detail": SEARCH_QUERY_ERROR},
            status=HTTP_400_BAD_REQUEST
        )

    indicators = Indicator.objects.filter(value__contains=query)

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

        return Response(status=200, data={
            'created-at': result.created_at,
            'created-by': result.created_by,
            'results': [
                {
                    'id': indicator.id,
                    'feed-name': feed['name'],
                    'feed-provider': feed['provider'],
                    'context': indicator.context
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