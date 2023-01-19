"""Views for search app"""

from json import loads

from django.views.decorators.http import require_http_methods
from django.core import serializers

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)

from console_api.constants import CREDS_ERROR, SEARCH_QUERY_ERROR
from console_api.services import CustomTokenAuthentication

from console_api.search.models import History, Indicator
from console_api.search.serializers import SearchHistorySerializer
from console_api.search.enums import SearchStatus


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
            'created_at': result.created_at,
            'created_by': result.created_by,
            'results': [
                {
                    'id': indicator.id,
                    'feed_name': feed['name'],
                    'feed_provider': feed['provider'],
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
            'created_at': item.created_at,
            'created_by': item.created_by,
            'query': item.query_text
        } for item in search_history
    ])
