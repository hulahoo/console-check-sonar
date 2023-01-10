from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from console_api.apps.source.models import Source
from console_api.api.source.serializers import SourceSerializer
from console_api.api.services import CustomTokenAuthentication


class SourceView(viewsets.ModelViewSet):
    serializer_class = SourceSerializer
    queryset = Source.objects.all()
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
