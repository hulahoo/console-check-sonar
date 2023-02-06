"""Views for context_sources app"""

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from console_api.context_sources.models import ContextSources
from console_api.context_sources.serializers import ContextSourcesListSerializer
from console_api.services import (
    CustomTokenAuthentication,
    get_response_with_pagination,
)


class ContextSourcesListView(ListAPIView):
    """Context sources list"""

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = ContextSources.objects.all()
    serializer_class = ContextSourcesListSerializer

    def list(self, request: Request, *args, **kwargs) -> Response:
        """Return response with list of context sources"""

        return get_response_with_pagination(
            request,
            self.queryset,
            self.get_serializer,
        )
