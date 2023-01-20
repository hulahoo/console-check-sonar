"""Views for feed app"""

from requests import get

from django.conf import settings
from rest_framework import status
from rest_framework.request import Request
from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from console_api.feed.models import Feed
from console_api.feed.serializers import (
    FeedSerializer,
    FeedsListSerializer,
)
from console_api.services import get_response_with_pagination
from console_api.services import CustomTokenAuthentication


class FeedView(APIView):
    """View for feed creation or get feeds list"""

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs) -> Response:

        feed = FeedSerializer(data=request.data)

        if feed.is_valid():
            try:
                feed.save()
                feed_id = Feed.objects.get(title=request.data["feed-name"]).id

                return Response({"id": feed_id}, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                return Response({"detail": e}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(status=status.HTTP_400_BAD_REQUEST)

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
        serializer = FeedSerializer(
            feed,
            data=request.data,
            partial=True,
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(status=status.HTTP_201_CREATED)
