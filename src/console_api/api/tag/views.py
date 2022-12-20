from rest_framework import viewsets

from console_api.apps.tag.models import Tag
from console_api.api.tag.serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
