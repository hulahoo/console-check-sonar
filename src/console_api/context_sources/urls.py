"""Urls for context_sources app"""

from django.urls import path
from rest_framework.routers import DefaultRouter

from console_api.context_sources.views import (
    ContextSourceDetailView,
    ContextSourcesView,
)


router = DefaultRouter()
router.register("", ContextSourcesView)

urlpatterns = [
    # Detail for context source
    path(
        "/<int:source_id>",
        ContextSourceDetailView.as_view(),
        name="context_source_detail",
    ),
]

urlpatterns += router.urls
