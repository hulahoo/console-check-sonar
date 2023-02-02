"""Views for feed app"""

from os import environ
from requests import get

from django.conf import settings
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.generics import ListAPIView

from console_api.feed.models import Feed
from console_api.feed.serializers import (
    FeedSerializer,
    FeedsListSerializer,
)
from console_api.services import (
    CustomTokenAuthentication,
    create_audit_log_entry,
    get_feed_logging_data,
    get_response_with_pagination,
)


class UpdateFeedsNowView(APIView):
    """Update feeds now"""

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs) -> Response:
        tip_feeds_import_worker_host = environ.get(
            "TIP_FEEDS_IMPORT_WORKER_HOST",
            "https://develop.tip-feeds-import-worker.rshb.axept.com",
        )

        feeds_update_url = f"{tip_feeds_import_worker_host}/api/force-update"

        try:
            get(feeds_update_url)
        except Exception as error:
            return Response({"detail": str(error)}, status=HTTP_400_BAD_REQUEST)

        return Response("Updated", status=HTTP_201_CREATED)


class ProvidersListView(ListAPIView):
    """List with feeds providers"""

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request: Request, *args, **kwargs) -> Response:
        """Return list with providers"""

        feeds = Feed.objects.all().order_by("provider").distinct("provider")

        return Response([feed.provider for feed in feeds], status=HTTP_200_OK)


class FeedView(APIView):
    """View for feed creation or get feeds list"""

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs) -> Response:

        feed = FeedSerializer(data=request.data)

        if feed.is_valid():
            feed.save()
            feed = Feed.objects.get(title=request.data["feed-name"])

            create_audit_log_entry(request, {
                "table": "feeds",
                "event_type": "create-feed",
                "object_type": "feed",
                "object_name": "Feed",
                "description": "Create a new feed",
                "new_value": get_feed_logging_data(feed),
            })

            return Response({"id": feed.id}, status=status.HTTP_201_CREATED)

        return Response(feed.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request: Request, *args, **kwargs) -> Response:
        return get_response_with_pagination(
            request=request,
            objects=Feed.objects.all(),
            serializer=FeedsListSerializer,
        )


class FeedPreview(APIView):

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, *args, **kwargs) -> Response:

        url = request.GET.get("url", None)
        if not url:
            return Response(
                {"detail": "URL not specified"},
                status=status.HTTP_400_BAD_REQUEST,
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
        response = get(url_for_get_preview, params=payload)

        return Response(response.content, status=response.status_code)


class FeedUpdate(APIView):

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs) -> Response:
        feed_id = kwargs.get("feed_id")

        if not Feed.objects.filter(id=feed_id).exists():
            return Response(
                {"detail": f"Feed with id {feed_id} doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        feed = Feed.objects.get(id=feed_id)

        prev_feed_value = get_feed_logging_data(feed)
        serializer = FeedSerializer(
            feed,
            data=request.data,
            partial=True,
            fields=request.data.keys()
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        create_audit_log_entry(request, {
            "table": "feeds",
            "event_type": "update-feed",
            "object_type": "feed",
            "object_name": "Feed",
            "description": "Update feed",
            "prev_value": prev_feed_value,
            "new_value": get_feed_logging_data(feed),
        })

        return Response(status=status.HTTP_201_CREATED)

