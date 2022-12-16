from rest_framework import viewsets

from console_api.apps.source.models import Source
from console_api.api.source.serializers import SourceSerializer


class SourceView(viewsets.ModelViewSet):
    serializer_class = SourceSerializer
    queryset = Source.objects.all()
