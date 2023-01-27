"""Views for detections app"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from console_api.detections.models import Detection
from console_api.detections.serializers import DetectionSerializer
from console_api.services import (
    CustomTokenAuthentication,
    get_filter_query_param,
    get_response_with_pagination,
    get_sort_by_param,
)


class DetectionListView(generics.ListAPIView):
    """View for detections list"""

    serializer_class = DetectionSerializer
    queryset = Detection.objects.all()

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def __filter_queryset(self, request: Request) -> None:
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

    def __sort_queryset(self, request: Request) -> None:
        """Sort the queryset"""

        if sort_by := get_sort_by_param(request):
            self.queryset = self.queryset.order_by(sort_by)

    def list(self, request: Request, *args, **kwargs) -> Response:
        """Return response with list of detections"""

        self.__filter_queryset(request)
        self.__sort_queryset(request)

        return get_response_with_pagination(
            request, self.queryset, self.get_serializer,
        )
