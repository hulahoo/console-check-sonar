"""Views for detections app"""

from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from console_api.detections.models import Detection, DetectionFeedRelationship
from console_api.detections.serializers import DetectionSerializer
from console_api.services import (
    CustomTokenAuthentication,
    get_filter_query_param,
    get_response_with_pagination,
)
from console_api.mixins import SortAndFilterQuerysetMixin
from console_api.feed.models import Feed


class DetectionListView(ListAPIView, SortAndFilterQuerysetMixin):
    """View for detections list"""

    _SORT_BY_PARAMS = (
        "id",
        "-id",
        "source",
        "-source",
        "source_message",
        "-source_message",
        "indicator_id",
        "-indicator_id",
        "detection_message",
        "-detection_message",
        "tags_weight",
        "-tags_weight",
        "indicator_weight",
        "-indicator_weight",
        "created_at",
        "-created_at",
    )

    serializer_class = DetectionSerializer
    queryset = Detection.objects.all()

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def __filter_by_feed_name(self, request: Request) -> None:
        if feed_name := get_filter_query_param(request, "query"):
            if not Feed.objects.filter(title=feed_name).exists():
                self.queryset = self.queryset.filter(
                    Q(source__icontains=feed_name)
                    | Q(details__icontains=feed_name)
                )
            else:
                feed_id = Feed.objects.get(title=feed_name).id

                detections_ids = [
                    rel.detection_id for rel in
                    DetectionFeedRelationship.objects.filter(feed_id=feed_id)
                ]

                self.queryset = self.queryset.filter(
                    Q(id__in=detections_ids)
                    | Q(source__icontains=feed_name)
                    | Q(details__icontains=feed_name)
                )

    def _filter_queryset(self, request: Request) -> None:
        """Filter the queryset"""

        detection_event = get_filter_query_param(request, "detection-event")
        detection_message = get_filter_query_param(request, "detection-message")
        indicator_weight = get_filter_query_param(request, "indicator-weight")

        if detection_id := get_filter_query_param(request, "id"):
            self.queryset = self.queryset.filter(id=detection_id)

        if source := get_filter_query_param(request, "source"):
            self.queryset = self.queryset.filter(source=source)

        if source_message := get_filter_query_param(request, "source-message"):
            self.queryset = self.queryset.filter(source_message=source_message)

        if details := get_filter_query_param(request, "details"):
            self.queryset = self.queryset.filter(details=details)

        if source_event := get_filter_query_param(request, "source-event"):
            self.queryset = self.queryset.filter(source_event=source_event)

        if indicator_id := get_filter_query_param(request, "indicator-id"):
            self.queryset = self.queryset.filter(indicator_id=indicator_id)

        if tags_weight := get_filter_query_param(request, "tags-weight"):
            self.queryset = self.queryset.filter(tags_weight=tags_weight)

        if created_at := get_filter_query_param(request, "created-at"):
            self.queryset = self.queryset.filter(created_at=created_at)

        if indicator_weight:
            self.queryset = self.queryset.filter(
                indicator_weight=indicator_weight,
            )

        if detection_event:
            self.queryset = self.queryset.filter(
                detection_event=detection_event,
            )

        if detection_message:
            self.queryset = self.queryset.filter(
                detection_message=detection_message,
            )

        self.__filter_by_feed_name(request)

    def list(self, request: Request, *args, **kwargs) -> Response:
        """Return response with list of detections"""

        response_or_none = self.get_error_or_sort_and_filter_queryset(
            request, *args, **kwargs
        )

        if isinstance(response_or_none, Response):
            return response_or_none

        return get_response_with_pagination(
            request, self.queryset, self.get_serializer,
        )
