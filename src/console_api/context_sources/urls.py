"""Urls for context_sources app"""

from console_api.context_sources.views import ContextSourcesView

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("", ContextSourcesView)

urlpatterns = []

urlpatterns += router.urls
