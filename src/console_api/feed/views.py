"""Views for feed app"""

from requests import get

from django.conf import settings
from django.db.utils import IntegrityError
from django.views.decorators.http import (
    require_http_methods,
    require_safe,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_406_NOT_ACCEPTABLE,
)

from console_api.constants import CREDENTIALS_ERROR
from console_api.feed.models import Feed
from console_api.feed.serializers import (
    FeedCreateSerializer,
    FeedsListSerializer,
    FeedUpdatePropertiesSerializer,
)
from console_api.services import (
    CustomTokenAuthentication,
    get_response_with_pagination,
)


@api_view(["POST", "GET"])
@require_http_methods(["GET", "POST"])
def feeds_view(request: Request) -> Response:
    """View for /feeds endpoint"""

    if not CustomTokenAuthentication().authenticate(request):
        return Response(
            {"detail": CREDENTIALS_ERROR},
            status=HTTP_403_FORBIDDEN
        )

    if request.method == "POST":
        feed = FeedCreateSerializer(data=request.data)

        if feed.is_valid():
            try:
                feed.save()
                feed_id = Feed.objects.get(title=request.data["feed-name"]).id

                return Response({"id": feed_id}, status=HTTP_201_CREATED)
            except IntegrityError as e:
                return Response({"detail": e}, status=HTTP_406_NOT_ACCEPTABLE)

    elif request.method == "GET":
        return get_response_with_pagination(
            request=request,
            objects=Feed.objects.all(),
            serializer=FeedsListSerializer,
        )

    return Response(feed.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@require_safe
def get_feed_preview(request: Request) -> Response:
    """Get feed preview"""

    if not CustomTokenAuthentication().authenticate(request):
        return Response(
            {"detail": CREDENTIALS_ERROR},
            status=HTTP_403_FORBIDDEN
        )

    url = request.GET.get("url", None)
    if not url:
        return Response(status=HTTP_400_BAD_REQUEST)

    auth_type = request.GET.get("auth_type", None)
    auth_login = request.GET.get("auth_login", None)
    auth_pass = request.GET.get("auth_pass", None)

    payload = {'url': url,
               'auth_type': auth_type,
               'auth_login': auth_login,
               'auth_pass': auth_pass}

    url_for_get_preview = settings.FEEDS_IMPORTING_SERVICE_URL + '/api/preview'
    r = get(url_for_get_preview, params=payload)

    return Response(r.content, status=r.status_code)


@api_view(("POST",))
@require_http_methods(["POST"])
def change_feed_properties_view(request: Request, feed_id: int) -> Response:
    """Change properties for the feed"""

    if not CustomTokenAuthentication().authenticate(request):
        return Response(
            {"detail": CREDENTIALS_ERROR},
            status=HTTP_403_FORBIDDEN
        )

    if not request.data:
        return Response(
            {"detail": "Feed data not specified"},
            status=HTTP_400_BAD_REQUEST,
        )

    feed = Feed.objects.filter(id=feed_id).first()
    if not feed:
        return Response(
            {"error": "Feed doesn't exists"},
            status=HTTP_400_BAD_REQUEST,
        )

    serializer = FeedUpdatePropertiesSerializer(feed, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)
    else:
        return Response(
            {"error": "Wrong data received"},
            status=HTTP_400_BAD_REQUEST,
        )
