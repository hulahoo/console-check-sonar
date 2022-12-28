"""Views for detections app"""

from rest_framework import generics

from console_api.apps.detections.models import Detection
from console_api.api.detections.serializers import DetectionSerializer
from console_api.api.services import (
    get_filter_query_param,
    get_response_with_pagination,
)


class DetectionListView(generics.ListAPIView):
    """View for detections list"""

    def list(self, request, *args, **kwargs):
        id_ = get_filter_query_param(request, "id")
        source_message = get_filter_query_param(request, "source-message")
        source_event = get_filter_query_param(request, "source-event")
        indicator_id = get_filter_query_param(request, "indicator-id")
        detection_event = get_filter_query_param(request, "detection-event")
        detection_message = get_filter_query_param(request, "detection-message")
        tags_weight = get_filter_query_param(request, "tags-weight")
        indicator_weight = get_filter_query_param(request, "indicator-weight")
        created_at = get_filter_query_param(request, "created-at")

        if id_:
            self.queryset = self.queryset.filter(id=id_)
        if source_message:
            self.queryset = self.queryset.filter(source_message=source_message)
        if source_event:
            self.queryset = self.queryset.filter(source_event=source_event)
        if indicator_id:
            self.queryset = self.queryset.filter(indicator_id=indicator_id)
        if detection_event:
            self.queryset = self.queryset.filter(detection_event=detection_event)
        if detection_message:
            self.queryset = self.queryset.filter(detection_message=detection_message)
        if tags_weight:
            self.queryset = self.queryset.filter(tags_weight=tags_weight)
        if indicator_weight:
            self.queryset = self.queryset.filter(indicator_weight=indicator_weight)
        if created_at:
            self.queryset = self.queryset.filter(created_at=created_at)

        if sort_by_param := request.GET.get('sort-by'):
            sort_by_param = sort_by_param[0] + sort_by_param[1:].replace('-', '_')
            self.queryset = self.queryset.order_by(sort_by_param)

        return get_response_with_pagination(
            request, self.queryset, self.get_serializer,
        )

    serializer_class = DetectionSerializer
    queryset = Detection.objects.all()
