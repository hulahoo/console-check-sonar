"""Urls for files app"""

from django.urls import path

from console_api.files.views import FilesView

urlpatterns = [
    path(
        "/<str:bucket>/<str:key>",
        FilesView.as_view(),
        name="file_upload",
    ),
]
