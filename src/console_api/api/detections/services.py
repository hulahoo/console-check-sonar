"""Services for detections app"""

from django.conf import settings
from django.db.models.query import QuerySet
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import SerializerMetaclass


def get_response_with_pagination(
        request: Request,
        objects: QuerySet,
        serializer: SerializerMetaclass) -> Response:
    """Return paginated response"""

    paginator = PageNumberPagination()

    paginator.page_size = _get_page_size(request)

    result_page = paginator.paginate_queryset(objects, request)

    return paginator.get_paginated_response(
        serializer(result_page, many=True).data,
    )


def _get_page_size(request: Request) -> int:
    """Return page size for pagination"""

    page_size = request.GET.get('page-size')

    if not page_size or int(page_size) <= 0:
        page_size = settings.REST_FRAMEWORK['PAGE_SIZE']

    return int(page_size)
