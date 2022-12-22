"""Views for detections app"""

from rest_framework import generics

from console_api.apps.detections.models import Detection
from src.console_api.api.detections.serializers import DetectionSerializer
from console_api.api.services import get_response_with_pagination


class DetectionListView(generics.ListAPIView):
    """View for detections list"""

    def list(self, request, *args, **kwargs):
        id_ = request.GET.get('filter[id]')
        source_event = request.GET.get('filter[source_event]')
        indicator = request.GET.get('filter[indicator]')
        tags_weight = request.GET.get('filter[tags_weight]')
        created_at = request.GET.get('filter[created_at]')

        if id_:
            self.queryset = self.queryset.filter(id=id_)
        if source_event:
            self.queryset = self.queryset.filter(source_event=source_event)
        if indicator:
            self.queryset = self.queryset.filter(indicator=indicator)
        if created_at:
            self.queryset = self.queryset.filter(created_at=created_at)
        if tags_weight:
            self.queryset = self.queryset.filter(tags_weight=tags_weight)

        sort_by_param = request.GET.get('sort-by')
        if sort_by_param:
            sort_by_param = sort_by_param[0] + sort_by_param[1:].replace('-', '_')
            self.queryset = self.queryset.order_by(sort_by_param)

        return get_response_with_pagination(
            request, self.queryset, self.get_serializer,
        )

    serializer_class = DetectionSerializer
    queryset = Detection.objects.all()
