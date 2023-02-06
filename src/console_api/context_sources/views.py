"""Views for context_sources app"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from console_api.context_sources.models import ContextSources
from console_api.context_sources.serializers import (
    ContextSourcesListSerializer,
)
from console_api.services import (
    CustomTokenAuthentication,
    create_audit_log_entry,
    get_response_with_pagination,
)


class ContextSourcesView(ModelViewSet):
    """Context sources view for get list and creation"""

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = ContextSources.objects.all()

    def list(self, request: Request, *args, **kwargs) -> Response:
        """Return response with list of context sources"""

        return get_response_with_pagination(
            request,
            self.queryset,
            ContextSourcesListSerializer,
        )

    def create(self, request: Request, *args, **kwargs) -> Response:
        """Create a context source"""

        if not request.data:
            return Response(
                {"detail": "Missing fields"},
                status=HTTP_400_BAD_REQUEST,
            )

        if ContextSources.objects.count() == 0:
            new_id = 1
        else:
            new_id = ContextSources.objects.order_by("id").last().id + 1

        ioc_type = request.data.get("ioc-type")
        source_url = request.data.get("source-url")
        request_method = request.data.get("request-method")
        request_headers = request.data.get("request-headers")
        request_body = request.data.get("request-body")
        inbound_removable_prefix = request.data.get("inbound-removable-prefix")
        outbound_appendable_prefix = request.data.get("outbound-appendable-prefix")
        created_by = request.data.get("created-by")

        ContextSources.objects.create(
            id=new_id,
            ioc_type=ioc_type,
            source_url=source_url,
            request_method=request_method,
            request_headers=request_headers,
            request_body=request_body,
            inbound_removable_prefix=inbound_removable_prefix,
            outbound_appendable_prefix=outbound_appendable_prefix,
            created_by=created_by,
        )

        create_audit_log_entry(request, {
            "table": "Console API | context_sources",
            "event_type": "create-context-sources",
            "object_type": "context source",
            "object_name": "Context source",
            "description": "Create a new context source",
            "new_value": {
                "id": new_id,
                "ioc-type": ioc_type,
                "source-url": source_url,
                "request-method": request_method,
                "request-headers": request_headers,
                "request-body": request_body,
                "inbound-removable-prefix": inbound_removable_prefix,
                "outbound-appendable-prefix": outbound_appendable_prefix,
                "created-by": created_by,
            },
        })

        return Response(status=HTTP_201_CREATED)
