"""Views for search app"""

from django.core import serializers
from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_501_NOT_IMPLEMENTED,
)

from console_api.search.models import History
from console_api.services import (
    CustomTokenAuthentication,
    get_response_with_pagination,
)
from console_api.search.serializers import (
    SearchHistorySerializer,
    SearchHistoryListSerializer,
)
from console_api.tag.models import Tag
from console_api.search.services import (
    get_creds_error_response,
    get_detections_by_query,
    get_detections_search_results,
    get_indicators_by_query,
    get_indicators_search_results,
    get_search_history,
    get_search_query_error_response,
    get_search_results_response,
)


@api_view(["GET"])
@require_http_methods(["GET"])
def search_detections_by_text_view(request: Request) -> Response:
    """Search detections by text"""

    if not CustomTokenAuthentication().authenticate(request):
        return get_creds_error_response()

    user, _ = CustomTokenAuthentication().authenticate(request)

    query = request.GET.get("query")

    if not query:
        return get_search_query_error_response()

    detections = get_detections_by_query(query)

    fields = ("id", "source", "source_message", "detection_message")
    search_history = get_search_history(query, detections, fields, user.id)

    search_results = get_detections_search_results(detections)

    return get_search_results_response(search_history, search_results)


@api_view(["GET"])
@require_http_methods(["GET"])
def search_indicators_view(request: Request) -> Response:
    """Search indicators"""

    if not CustomTokenAuthentication().authenticate(request):
        return get_creds_error_response()

    user, _ = CustomTokenAuthentication().authenticate(request)

    query_type = request.GET.get("query-type")
    value = request.GET.get("value")

    if not query_type or not value:
        return Response(
            {"detail": "query-type or value param not specified"},
            status=HTTP_400_BAD_REQUEST,
        )

    if query_type not in ("log-file", "file", "text"):
        return Response(
            {"detail": "Wrong query-type"}, status=HTTP_400_BAD_REQUEST
        )

    if query_type == "log-file":
        return Response(status=HTTP_501_NOT_IMPLEMENTED)

    indicators = get_indicators_by_query(query_type, value)

    search_history = get_search_history(
        f"{query_type}, {value}", indicators, ("id", "value"), user.id
    )

    search_results = get_indicators_search_results(indicators)

    return get_search_results_response(search_history, search_results)


@api_view(["GET"])
@require_http_methods(["GET"])
def search_history_view(request: Request) -> Response:
    """Return search history"""

    if not CustomTokenAuthentication().authenticate(request):
        return get_creds_error_response()

    return get_response_with_pagination(
        request,
        History.objects.all(),
        SearchHistoryListSerializer,
    )


class SearchTagsView(APIView):

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, *args, **kwargs) -> Response:
        query = request.GET.get("query")

        if not query:
            return get_search_query_error_response()

        tags: list[Tag] = Tag.objects.filter(title__contains=query)

        search_history = SearchHistorySerializer(
            data={
                "search_type": "by-title",
                "query_text": query,
                "query_data": None,
                "results": serializers.serialize(
                    "json",
                    tags,
                    fields=("id", "title"),
                ),
                "created_by": request.user.id,
            }
        )

        if search_history.is_valid():
            result = search_history.save()

            return Response(
                status=HTTP_200_OK,
                data={
                    "created-at": result.created_at,
                    "created-by": result.created_by,
                    "results": [
                        {
                            "id": tag.id,
                            "title": tag.title,
                            "weight": tag.weight,
                            "created-by": tag.created_by,
                            "created-at": tag.created_at,
                        }
                        for tag in tags
                    ],
                },
            )
