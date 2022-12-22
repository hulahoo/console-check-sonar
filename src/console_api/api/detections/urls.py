"""Urls for detections app"""

from django.urls import path

from console_api.api.detections.views import DetectionListView


urlpatterns = [
    path('', DetectionListView.as_view(), name='detections'),
]
