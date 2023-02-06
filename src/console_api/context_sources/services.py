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
