"""Views for source app"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from console_api.services import CustomTokenAuthentication
from console_api.source.models import Source
from console_api.source.serializers import SourceSerializer


class SourceView(viewsets.ModelViewSet):
    """View for Source model"""

    serializer_class = SourceSerializer
    queryset = Source.objects.all()
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
