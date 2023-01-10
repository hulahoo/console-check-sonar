from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from console_api.apps.tag.models import Tag
from console_api.api.tag.serializers import TagSerializer
from console_api.api.services import CustomTokenAuthentication


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
