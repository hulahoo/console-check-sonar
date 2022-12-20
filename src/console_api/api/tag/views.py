from rest_framework import viewsets

from apps.tag.models import Tag
from api.tag.serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
