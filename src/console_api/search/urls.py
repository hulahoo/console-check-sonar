"""Urls for search app"""

from django.urls import path

from console_api.search.views import search_by_text_view, search_history_view


urlpatterns = [
    path(
        "/history",
        search_history_view,
        name="history",
    ),
    path(
        "/by-text",
        search_by_text_view,
        name="by_text",
    ),
]
