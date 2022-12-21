"""Urls for detections app"""

from django.urls import path

from api.detections.views import DetectionListView


urlpatterns = [
    path('', DetectionListView.as_view(), name='detections'),
]
