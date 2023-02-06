"""Urls for context_sources app"""

from django.urls import path

from console_api.context_sources.views import ContextSourcesListView


urlpatterns = [
    path("", ContextSourcesListView.as_view(), name="context_sources_list"),
]
