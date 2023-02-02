"""Views for audit_logs app"""

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from console_api.audit_logs.models import AuditLogs
from console_api.audit_logs.serializers import AuditLogsListSerializer
from console_api.services import (
    CustomTokenAuthentication,
    get_filter_query_param,
    get_response_with_pagination,
    get_sort_by_param,
)


class AuditLogsListView(ListAPIView):
    """Audit logs list"""

    __SORT_BY_PARAMS = (
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

    def __filter_queryset(self, request: Request) -> None:
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

        try:
            self.__filter_queryset(request)

            if sort_by := get_sort_by_param(request):
                if sort_by not in self.__SORT_BY_PARAMS:
                    return Response(
                        {"detail": "Wrong value for sort-by parameter"},
                        status=HTTP_400_BAD_REQUEST,
                    )

                self.queryset = self.queryset.order_by(sort_by)
        except Exception as error:
            return Response(
                {"detail": str(error)},
                status=HTTP_400_BAD_REQUEST,
            )

        return get_response_with_pagination(
            request,
            self.queryset,
            self.get_serializer,
        )
