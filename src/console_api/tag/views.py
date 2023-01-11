"""Views for tag app"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from console_api.tag.models import Tag
from console_api.tag.serializers import TagSerializer
from console_api.services import CustomTokenAuthentication


class TagViewSet(viewsets.ModelViewSet):
    """Viewset for tags"""

    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
