"""Services for project"""

from hashlib import sha256

from django.conf import settings
from django.db.models.query import QuerySet
from rest_framework.authentication import BaseAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import SerializerMetaclass
from rest_framework.status import HTTP_400_BAD_REQUEST

from console_api.audit_logs.models import AuditLogs
from console_api.users.models import User, Token


def get_not_fields_error(
        request: Request, expected_fields: tuple) -> None | Response:
    """Check if fields exists and return response with 400 erorr if not"""

    for field in expected_fields:
        if not request.data.get(field):
            return Response(
                {"detail": f"{field} not specified"},
                status=HTTP_400_BAD_REQUEST,
            )

    return None


def create_audit_log_entry(request: Request, data: dict) -> None:
    """Create an entry to audit_logs table for user's action"""

    if User.objects.filter(id=request.user.id):
        user_name = User.objects.get(id=request.user.id)
    else:
        user_name = None

    if AuditLogs.objects.count() == 0:
        new_id = 1
    else:
        new_id = AuditLogs.objects.order_by("id").last().id + 1

    AuditLogs.objects.create(
        id=new_id,
        service_name=f"Console API {data.get('table', '')}",
        user_id=request.user.id,
        user_name=user_name,
        event_type=data.get("event_type"),
        object_type=data.get("object_type"),
        object_name=data.get("object_name"),
        description=data.get("description"),
        prev_value=data.get("prev_value"),
        new_value=data.get("new_value"),
        context={
            "User Agent": request.META.get("HTTP_USER_AGENT"),
            "URL": request.META.get("RAW_URI"),
            "IP": request.META.get("REMOTE_ADDR"),
            "Protocol": request.META.get("SERVER_PROTOCOL"),
        },
    )


def get_hashed_password(password: str):
    """Return hashed password (SHA256)"""

    return sha256(bytes(password.encode())).hexdigest()


class CustomTokenAuthentication(BaseAuthentication):
    """Custom token authentication class"""

    def authenticate(self, request):
        if token := request.META.get("HTTP_AUTHORIZATION"):
            token = token.split()
            if len(token) > 1:
                token = token[1]
            else:
                return None

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

    page_size = request.GET.get("page-size")

    if not page_size or int(page_size) <= 0:
        page_size = settings.REST_FRAMEWORK["PAGE_SIZE"]

    return int(page_size)


def get_filter_query_param(request, field: str) -> str:
    """Return filter query parameter for the field"""

    return request.GET.get(f"filter[{field}]")
