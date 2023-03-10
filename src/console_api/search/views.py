"""Views for search app"""
import secrets


from urllib import parse


from urllib import parse

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
    HTTP_404_NOT_FOUND,
    HTTP_202_ACCEPTED
)

from console_api.files.models import Files
from console_api.search.models import History
from console_api.services import (
    CustomTokenAuthentication,
    get_response_with_pagination,
    get_sort_by_param,
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

    query_type = request.GET.get("query-type", "text")

    if query_type == "log-file":
        return Response(status=HTTP_501_NOT_IMPLEMENTED)
    elif query_type == "hashes":
        values = request.GET.get("values")

        if not values:
            return Response(
                {"detail": "values param not specified"},
                status=HTTP_400_BAD_REQUEST,
            )

        values = parse.unquote(values)

        values = values.replace("[", "").replace("]", "").replace(
            " ", ""
        ).replace('"', '')
        values = values.split(",")
    elif query_type == "text":
        if value := request.GET.get("value"):
            values = [value]
        else:
            return Response(
                {"detail": "value param not specified"},
                status=HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(
            {"detail": "Wrong query-type"}, status=HTTP_400_BAD_REQUEST
        )

    indicators = get_indicators_by_query(query_type, values)

    search_history = get_search_history(
        f"{query_type}, {values}", indicators, ("id", "value"), user.id
    )

    search_results = get_indicators_search_results(indicators)

    return get_search_results_response(search_history, search_results)


@api_view(["GET"])
@require_http_methods(["GET"])
def search_history_view(request: Request) -> Response:
    """Return search history"""

    if not CustomTokenAuthentication().authenticate(request):
        return get_creds_error_response()

    queryset = History.objects.all()

    if sort_by := get_sort_by_param(request):
        queryset = queryset.order_by(sort_by)

    return get_response_with_pagination(
        request, queryset, SearchHistoryListSerializer
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


@api_view(["GET"])
@require_http_methods(["GET"])
def file_search_job_status(request: Request, *args, **kwargs) -> Response:
    if not CustomTokenAuthentication().authenticate(request):
        return get_creds_error_response()

    job_id = request.GET.get("job-id")

    return Response(status=HTTP_200_OK, data={'status': f'{job_id} in progress'})


@api_view(["GET"])
@require_http_methods(["GET"])
def file_search_job_result(request: Request, *args, **kwargs) -> Response:
    if not CustomTokenAuthentication().authenticate(request):
        return get_creds_error_response()

    job_id = request.GET.get("job-id")
    checked_obj = secrets.randbelow(10000)
    detection = secrets.randbelow(checked_obj / 2)

    return Response(status=HTTP_200_OK, data={'job-id': job_id,
                                              'checked-obj': checked_obj,
                                              'detection': detection})


@api_view(["POST"])
@require_http_methods(["POST"])
def file_search_start_job(request: Request, *args, **kwargs) -> Response:
    if not CustomTokenAuthentication().authenticate(request):
        return get_creds_error_response()

    key = request.POST.get("key")
    bucket = request.POST.get("bucket")

    instance = Files.objects.get(key=key, bucket=bucket)
    if not instance:
        return Response(status=HTTP_404_NOT_FOUND, data='File not found')

    job_id = secrets.randbelow(1000)

    return Response(status=HTTP_202_ACCEPTED, data={'job_id': job_id})


@api_view(["POST"])
@require_http_methods(["POST"])
def file_search_stop_job(request: Request, *args, **kwargs) -> Response:
    if not CustomTokenAuthentication().authenticate(request):
        return get_creds_error_response()

    job_id = request.POST.get("job_id")

    return Response(status=HTTP_200_OK, data={'job_id': job_id})
