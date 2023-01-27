"""Views for audit_logs app"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from console_api.audit_logs.models import AuditLogs
from console_api.audit_logs.serializers import AuditLogsSerializer
from console_api.services import (
    CustomTokenAuthentication,
    get_filter_query_param,
    get_response_with_pagination,
    get_sort_by_param,
)


class AuditLogsListView(generics.ListAPIView):
    """Audit logs list"""

    serializer_class = AuditLogsSerializer
    queryset = AuditLogs.objects.all()

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def __filter_queryset(self, request: Request) -> None:
        """Filter the queryset"""

        if created_at := get_filter_query_param(request, "created-at"):
            self.queryset = self.queryset.filter(created_at=created_at)

        if event_id := get_filter_query_param(request, "id"):
            self.queryset = self.queryset.filter(id=event_id)

        if service_name := get_filter_query_param(request, "service-name"):
            self.queryset = self.queryset.filter(service_name=service_name)

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

    def __sort_queryset(self, request: Request) -> None:
        """Sort the queryset"""

        if sort_by := get_sort_by_param(request):
            self.queryset = self.queryset.order_by(sort_by)

    def list(self, request: Request, *args, **kwargs) -> Response:
        """Return response with list of logs"""

        self.__filter_queryset(request)
        self.__sort_queryset(request)

        return get_response_with_pagination(
            request,
            self.queryset,
            self.get_serializer,
        )
