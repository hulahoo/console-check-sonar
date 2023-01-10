"""Views for feed app"""

from django.db.utils import IntegrityError
from django_filters import rest_framework as filters
from django.views.decorators.http import require_POST
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_406_NOT_ACCEPTABLE,
)
from rest_framework.permissions import IsAuthenticated

from console_api.api.services import (
    CustomTokenAuthentication,
    get_response_with_pagination,
)
from console_api.apps.feed.models import Feed
from console_api.api.feed.serializers import FeedSerializer, FeedListObjectSerializer
from console_api.apps.services.format_selector import choose_type


@api_view(["POST", "GET"])
def feed_add(request: Request):
    """Add feed"""

    if not CustomTokenAuthentication().authenticate(request):
        return Response(status=HTTP_403_FORBIDDEN)

    if request.method == "POST":
        serializer = FeedSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=HTTP_201_CREATED)
            except IntegrityError:
                data = {"detail": "Error during save data"}
                return Response(data, status=HTTP_406_NOT_ACCEPTABLE)
    if request.method == "GET":
        feeds_list = Feed.objects.all()
        return get_response_with_pagination(
            request=request,
            objects=feeds_list,
            serializer=FeedListObjectSerializer,
        )
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@require_POST
def feed_create(request):
    """Create feed"""

    if not CustomTokenAuthentication().authenticate(request):
        return Response(status=HTTP_403_FORBIDDEN)

    data = request.data
    feed = Feed(**data["feed"])
    method = choose_type(data["type"])
    config = data.get("config", {})
    results = method(feed, data["raw_indicators"], config)
    return Response({"results": results})


class FeedListView(viewsets.ModelViewSet):
    """View for list of feeds"""

    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
