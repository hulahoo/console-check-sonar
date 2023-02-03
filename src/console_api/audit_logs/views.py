"""Views for audit_logs app"""

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from console_api.audit_logs.models import AuditLogs
from console_api.audit_logs.serializers import AuditLogsListSerializer
from console_api.services import (
    CustomTokenAuthentication,
    get_filter_query_param,
    get_response_with_pagination,
)
from console_api.mixins import SortAndFilterQuerysetMixin


class AuditLogsListView(ListAPIView, SortAndFilterQuerysetMixin):
    """Audit logs list"""

    _SORT_BY_PARAMS = (
        "id",
        "-id",
        "service_name",
        "-service_name",
        "user_id",
        "-user_id",
        "user_name",
        "-user_name",
        "event_type",
        "-event_type",
        "object_type",
        "-object_type",
        "object_name",
        "-object_name",
        "description",
        "-description",
        "created_at",
        "-created_at",
    )

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = AuditLogs.objects.all()
    serializer_class = AuditLogsListSerializer

    def _filter_queryset(self, request: Request) -> None:
        """Filter the queryset"""

        if event_id := get_filter_query_param(request, "id"):
            self.queryset = self.queryset.filter(id=event_id)

        if service_name := get_filter_query_param(request, "service-name"):
            self.queryset = self.queryset.filter(service_name=service_name)

        if user_id := get_filter_query_param(request, "user-id"):
            self.queryset = self.queryset.filter(user_id=user_id)

        if user_name := get_filter_query_param(request, "user-name"):
            self.queryset = self.queryset.filter(user_name=user_name)

        if event_type := get_filter_query_param(request, "event-type"):
            self.queryset = self.queryset.filter(event_type=event_type)

        if object_type := get_filter_query_param(request, "object-type"):
            self.queryset = self.queryset.filter(object_type=object_type)

        if object_name := get_filter_query_param(request, "object-name"):
            self.queryset = self.queryset.filter(object_name=object_name)

        if description := get_filter_query_param(request, "description"):
            self.queryset = self.queryset.filter(description=description)

        if created_at := get_filter_query_param(request, "created-at"):
            self.queryset = self.queryset.filter(created_at=created_at)

    def list(self, request: Request, *args, **kwargs) -> Response:
        """Return response with list of logs"""

        response_or_none = self.get_error_or_sort_and_filter_queryset(
            request, *args, **kwargs
        )

        if isinstance(response_or_none, Response):
            return response_or_none

        return get_response_with_pagination(
            request,
            self.queryset,
            self.get_serializer,
        )
