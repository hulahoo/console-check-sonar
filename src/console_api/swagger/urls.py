"""Swagger urls"""

from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Console API",
        default_version="v3",
        description="Console API"
    ),
    permission_classes=(permissions.AllowAny,),
    patterns=[
        path("api/statistics/", include("console_api.api.statistics.urls")),
        path("api/users/", include("console_api.apps.users.urls")),
        path("api/feeds", include("console_api.api.feed.urls")),
        path("api/source/", include("console_api.api.source.urls")),
        path("api/tag/", include("console_api.api.tag.urls")),
        path("api/api/", include("console_api.api.system.urls")),
        path("api/detections/", include("src.console_api.api.detections.urls")),
        path("api/indicators/", include("console_api.api.indicator.urls")),
    ],
)

urlpatterns = [
    path(
        "api/doc/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-api-ui",
    ),
]
