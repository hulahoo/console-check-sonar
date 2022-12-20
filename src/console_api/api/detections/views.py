"""Views for detections app"""

from rest_framework import generics

from apps.detections.models import Detection
from api.detections.serializers import DetectionSerializer


class DetectionListView(generics.ListAPIView):
    """View for detections list"""

    serializer_class = DetectionSerializer
    queryset = Detection.objects.all()
