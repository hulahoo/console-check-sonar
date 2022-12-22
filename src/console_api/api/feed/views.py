from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_filters import rest_framework as filters

from console_api.apps.feed.models import Feed
from console_api.api.feed.serializers import FeedSerializer
from console_api.apps.services.format_selector import choose_type

from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST


@api_view(["POST"])
def feed_add(request):
    if request.method == "POST":
        serializer = FeedSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=HTTP_201_CREATED)

    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


def feed_create(request):
    data = request.data
    feed = Feed(**data["feed"])
    method = choose_type(data['type'])
    config = data.get('config', {})
    results = method(feed, data['raw_indicators'], config)
    return Response({'results': results})


class FeedListView(viewsets.ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    filter_backends = (filters.DjangoFilterBackend,)
