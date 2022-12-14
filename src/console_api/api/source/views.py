from rest_framework import viewsets

from apps.source.models import Source
from api.source.serializers import SourceSerializer


class SourceView(viewsets.ModelViewSet):
    serializer_class = SourceSerializer
    queryset = Source.objects.all()
