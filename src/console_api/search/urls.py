"""Urls for search app"""

from django.urls import path

from console_api.search.views import (
    by_text,
    history
)


urlpatterns = [
    path(
        "/history",
        history,
        name="history",
    ),
    path(
        "/by-text",
        by_text,
        name="by_text",
    ),
]
