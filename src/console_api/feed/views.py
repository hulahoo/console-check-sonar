"""Views for feed app"""

import json
from datetime import datetime
from requests import get, post

from django.conf import settings
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.generics import ListAPIView

from console_api.config.logger_config import logger
from console_api.feed.models import Feed, IndicatorFeedRelationship
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


class FeedsLastUpdateView(APIView):
    """Last feeds update view"""

    def get(self, request: Request, *args, **kwargs) -> Response:
        return Response(datetime.now().isoformat(), status=HTTP_200_OK)


class UpdateFeedsNowView(APIView):
    """Update feeds now"""

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs) -> Response:
        feeds_update_url = f"{settings.FEEDS_IMPORTING_SERVICE_URL}/api/force-update"

        try:
            get(feeds_update_url)
        except Exception as error:
            return Response({"detail": str(error)}, status=HTTP_400_BAD_REQUEST)

        create_audit_log_entry(request, {
            "table": "Feeds-importing-worker",
            "event_type": "update-feeds",
            "object_type": "feed",
            "object_name": "Feed",
            "description": "Update feeds",
        })

        return Response(status=HTTP_200_OK)


class FeedUpdateFrequency(APIView):
    """Set global frequency for feeds update"""

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    frequency_url = f"{settings.FEEDS_IMPORTING_SERVICE_URL}/api/current-frequency"

    def handler(self, data: str) -> Response:
        if not data:
            with get(self.frequency_url) as response:
                response.raise_for_status()
                return Response(json.loads(response.content), status=HTTP_200_OK)
        else:
            with post(self.frequency_url, json=data) as response:
                response.raise_for_status()
                return Response(status=HTTP_201_CREATED)

    def post(self, request: Request, *args, **kwargs) -> Response:
        create_audit_log_entry(request, {
            "table": "Feeds-importing-worker",
            "event_type": "update-feeds",
            "object_type": "feed",
            "object_name": "Feed",
            "description": f"Set frequency for feeds update to: {request.data.get('delay', 0)}min",
        })
        logger.info(f"Income data: {json.dumps(request.data)}")
        return self.handler(data=json.dumps(request.data))

    def get(self, request: Request, *args, **kwargs) -> Response:
        create_audit_log_entry(request, {
            "table": "Feeds-importing-worker",
            "event_type": "update-feeds",
            "object_type": "feed",
            "object_name": "Feed",
            "description": "Get frequency update detail"
        })

        return self.handler(data=request.data)


class ProvidersListView(ListAPIView):
    """List with feeds providers"""

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request: Request, *args, **kwargs) -> Response:
        """Return list with providers"""

        feeds = Feed.objects.filter(is_deleted=False).order_by("provider").distinct("provider")

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
                "table": "Console API | feeds",
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
            objects=Feed.objects.filter(is_deleted=False),
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
            "table": "Console API | feeds",
            "event_type": "update-feed",
            "object_type": "feed",
            "object_name": "Feed",
            "description": "Update feed",
            "prev_value": prev_feed_value,
            "new_value": get_feed_logging_data(feed),
        })

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        feed_id = kwargs.get("feed_id")
        now = datetime.now()

        if not Feed.objects.filter(id=feed_id).exists():
            return Response(
                {"detail": f"Feed with id {feed_id} doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        feed = Feed.objects.get(id=feed_id)
        try:
            feed.is_active = False
            feed.is_deleted = True
            feed.deleted_at = now
            feed.deleted_by = request.user.id
            feed.save()
            self.delete_indicator_feed_relationship(deleted_at=now, feed_id=feed.id)
        except Exception as e:
            return Response(
                {"detail": f"Error occured while deleting feed: {e.args}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(
            {"detail": "Feed deleted"},
            status=status.HTTP_200_OK
        )

    @staticmethod
    def delete_indicator_feed_relationship(deleted_at: datetime, feed_id: int):
        IndicatorFeedRelationship.objects.filter(
            feed_id=feed_id
        ).update(
            deleted_at=deleted_at
        )
