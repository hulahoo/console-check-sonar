"""Urls for search app"""

from django.urls import path

from console_api.search.views import (
    search_indicators_by_text_view,
    search_detections_by_text_view,
    search_history_view,
    SearchTagsView,
)


urlpatterns = [
    path(
        "/history",
        search_history_view,
        name="history",
    ),
    path(
        "/by-text",
        search_indicators_by_text_view,
        name="by_text",
    ),
    path(
        "/detections/by-text",
        search_detections_by_text_view,
        name="detections_by_text",
    ),
    path(
        "/tags/by-title",
        SearchTagsView.as_view(),
        name="tags_by_title"
    )
]
