"""Views for feed app"""

from requests import get

from django.conf import settings
from django.db.utils import IntegrityError
from django.views.decorators.http import require_http_methods, require_safe
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_406_NOT_ACCEPTABLE,
)

from console_api.constants import CREDS_ERROR
from console_api.feed.models import Feed
from console_api.feed.serializers import (
    FeedCreateUpdateSerializer,
    FeedsListSerializer,
)
from console_api.services import (
    CustomTokenAuthentication,
    get_response_with_pagination,
)


@require_http_methods(["GET", "POST"])
@api_view(["POST", "GET"])
def feeds_view(request: Request) -> Response:
    """View for /feeds endpoint"""

    if not CustomTokenAuthentication().authenticate(request):
        return Response({"detail": CREDS_ERROR}, status=HTTP_403_FORBIDDEN)

    if request.method == "POST":
        feed = FeedCreateUpdateSerializer(data=request.data)

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
def feed_preview_view(request: Request) -> Response:
    """Get feed preview"""

    if not CustomTokenAuthentication().authenticate(request):
        return Response({"detail": CREDS_ERROR}, status=HTTP_403_FORBIDDEN)

    url = request.GET.get("url", None)
    if not url:
        return Response(
            {"detail": "URL not specified"},
            status=HTTP_400_BAD_REQUEST,
        )

    auth_type = request.GET.get("auth-type", None)
    auth_login = request.GET.get("auth-login", None)
    auth_pass = request.GET.get("auth-pass", None)

    payload = {
        "url": url,
        "auth_type": auth_type,
        "auth_login": auth_login,
        "auth_pass": auth_pass,
    }

    url_for_get_preview = settings.FEEDS_IMPORTING_SERVICE_URL + "/api/preview"
    r = get(url_for_get_preview, params=payload)

    return Response(r.content, status=r.status_code)


@api_view(("POST",))
@require_http_methods(["POST"])
def update_feed_view(request: Request, feed_id: int) -> Response:
    """Update feed's fields"""

    if not CustomTokenAuthentication().authenticate(request):
        return Response({"detail": CREDS_ERROR}, status=HTTP_403_FORBIDDEN)

    if not Feed.objects.filter(id=feed_id).exists():
        return Response(
            {"detail": f"Feed with id {feed_id} doesn't exists"},
            status=HTTP_400_BAD_REQUEST,
        )

    feed = Feed.objects.get(id=feed_id)
    serializer = FeedCreateUpdateSerializer(
        feed,
        data=request.data,
        partial=True,
    )

    if not serializer.is_valid():
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    serializer.save()

    return Response(status=HTTP_201_CREATED)
