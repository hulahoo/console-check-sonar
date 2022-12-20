"""Views for detections app"""

from rest_framework import generics

from apps.detections.models import Detection
from api.detections.serializers import DetectionSerializer
from api.detections.services import get_response_with_pagination


class DetectionListView(generics.ListAPIView):
    """View for detections list"""

    def list(self, request, *args, **kwargs):
        return get_response_with_pagination(
            request, self.queryset, self.get_serializer,
        )

    serializer_class = DetectionSerializer
    queryset = Detection.objects.all()
