"""Services for context_sources app"""

from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.response import Response

from console_api.context_sources.models import ContextSources


def get_context_source_or_error_response(
        source_id: int) -> ContextSources | Response:
    """Return context source or response with 400 error if not exists"""

    return (
        ContextSources.objects.get(id=source_id)
        if ContextSources.objects.filter(id=source_id).exists()
        else Response(
            {"detail": f"Context source with id {source_id} doesn't exists"},
            status=HTTP_400_BAD_REQUEST,
        )
    )


def get_context_source_logging_data(source) -> dict:
    """Return context source data for logging"""

    return {
        "id": source.id,
        "ioc-type": source.ioc_type,
        "source-url": source.source_url,
        "request-method": source.request_method,
        "request-headers": source.request_headers,
        "request-body": source.request_body,
        "inbound-removable-prefix": source.inbound_removable_prefix,
        "outbound-appendable-prefix": source.outbound_appendable_prefix,
        "created-by": source.created_by,
    }
