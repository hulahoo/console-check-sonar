"""Services for api app"""

from django.conf import settings
from django.db.models.query import QuerySet
from rest_framework.authentication import BaseAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import SerializerMetaclass

from console_api.apps.users.models import User, Token


class CustomTokenAuthentication(BaseAuthentication):
    """Custom token authentication class"""

    def authenticate(self, request):
        if token := request.META.get('HTTP_AUTHORIZATION'):
            token = token.split()[1]

            if not Token.objects.filter(key=token).exists():
                return None

            user_id = Token.objects.get(key=token).user.id

            if User.objects.filter(id=user_id).exists():
                user = User.objects.get(id=user_id)

                # Authentication successful
                return user, None

        # Authentication failed
        return None


def get_response_with_pagination(
        request: Request,
        objects: QuerySet,
        serializer: SerializerMetaclass) -> Response:
    """Return paginated response"""

    paginator = PageNumberPagination()

    paginator.page_size = _get_page_size(request)
    paginator.page_query_param = "page-number"

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


def get_filter_query_param(request, field: str) -> str:
    """Return filter query parameter for the field"""

    return request.GET.get(f'filter[{field}]')
