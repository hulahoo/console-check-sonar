"""Views for audit_logs app"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from console_api.audit_logs.models import AuditLogs
from console_api.audit_logs.serializers import AuditLogsSerializer
from console_api.services import (
    CustomTokenAuthentication,
    get_filter_query_param,
    get_response_with_pagination,
)


class AuditLogsListView(generics.ListAPIView):
    """View for audit logs list"""

    def list(self, request, *args, **kwargs):
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

        if sort_by := request.GET.get("sort-by"):
            sort_by = sort_by[0] + sort_by[1:].replace("-", "_")
            self.queryset = self.queryset.order_by(sort_by)

        return get_response_with_pagination(
            request,
            self.queryset,
            self.get_serializer,
        )

    serializer_class = AuditLogsSerializer
    queryset = AuditLogs.objects.all()
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
