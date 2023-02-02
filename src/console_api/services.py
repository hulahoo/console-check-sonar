"""Services for project"""

from hashlib import sha256

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
from rest_framework.authentication import BaseAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import SerializerMetaclass
from rest_framework.status import HTTP_400_BAD_REQUEST

from console_api.audit_logs.models import AuditLogs
from console_api.users.models import User, Token


def run_field_attribute_test(
        model, self_,
        field_and_attribute_value: dict,
        attribute_name: str) -> None:
    """Test attribute value for all model's objects"""

    if not model.objects.exists():
        raise ObjectDoesNotExist(
            f'There is no test objects for {model.__name__} model'
        )

    for object_ in model.objects.all():
        for field, expected_value in field_and_attribute_value.items():
            with self_.subTest(f'{field=}'):
                real_value = getattr(
                    object_._meta.get_field(field), attribute_name,
                )

                self_.assertEqual(real_value, expected_value)


def get_sort_by_param(request: Request) -> str | None:
    """Return value for query parameter sort_by"""

    sort_by = request.GET.get("sort-by")

    if sort_by:
        sort_by = sort_by[0] + sort_by[1:].replace("-", "_")

    return sort_by


def get_indicator_logging_data(indicator) -> dict:
    """Return indicator data for logging"""

    if indicator.first_detected_at:
        first_detected_at = str(indicator.first_detected_at)
    else:
        first_detected_at = indicator.first_detected_at

    if indicator.last_detected_at:
        last_detected_at = str(indicator.last_detected_at)
    else:
        last_detected_at = indicator.last_detected_at

    return {
        "ioc_type": indicator.ioc_type,
        "value": indicator.value,
        "context": indicator.context,
        "is_sending_to_detections": indicator.is_sending_to_detections,
        "is_false_positive": indicator.is_false_positive,
        "weight": str(indicator.weight),
        "feeds_weight": str(indicator.feeds_weight),
        "time_weight": str(indicator.time_weight),
        "tags_weight": str(indicator.tags_weight),
        "is_archived": indicator.is_archived,
        "false_detected_counter": indicator.false_detected_counter,
        "positive_detected_counter": indicator.positive_detected_counter,
        "total_detected_counter": indicator.total_detected_counter,
        "first_detected_at": first_detected_at,
        "last_detected_at": last_detected_at,
        "created_by": indicator.created_by,
        "external_source_link": indicator.external_source_link,
        "created_at": str(indicator.created_at) if indicator.created_at else indicator.created_at,
        "updated_at": str(indicator.updated_at) if indicator.updated_at else indicator.updated_at,
        "deleted_at": str(indicator.deleted_at) if indicator.deleted_at else indicator.deleted_at,
    }


def get_feed_logging_data(feed) -> dict:
    """Return feed data for logging"""

    return {
        "id": feed.id,
        "title": feed.title,
        "provider": feed.provider,
        "description": feed.description,
        "format": feed.format,
        "weight": str(feed.weight),
        "status": feed.status,
        "created_at": str(feed.created_at),
    }


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

    if not request.GET.get("page-size", "0").isdigit():
        return Response(
            {"detail": "Invalid page-size parameter"},
            status=HTTP_400_BAD_REQUEST,
        )

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
