"""Urls for api app"""

from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

from console_api.apps.users.views import CustomAuthTokenView


schema_view = get_schema_view(
    openapi.Info(
        title="Console API",
        default_version="v3",
        description="Console API"
    ),
    permission_classes=(AllowAny,),
    patterns=[
        path("api/statistics/", include("console_api.api.statistics.urls")),
        path("api/users/", include("console_api.apps.users.urls")),
        path("api/feeds", include("console_api.api.feed.urls")),
        path("api/source/", include("console_api.api.source.urls")),
        path("api/tag/", include("console_api.api.tag.urls")),
        path("api/detections/", include("console_api.api.detections.urls")),
        path("api/indicators/", include("console_api.api.indicator.urls")),
    ],
)

urlpatterns = [
    path("feeds", include("console_api.api.feed.urls")),
    path("statistics", include("console_api.api.statistics.urls")),
    path("source", include("console_api.api.source.urls")),
    path("tag", include("console_api.api.tag.urls")),
    path("users", include("console_api.apps.users.urls")),
    path("detections", include("console_api.api.detections.urls")),
    path("sessions", CustomAuthTokenView.as_view()),
    path("indicators", include("console_api.api.indicator.urls")),
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-api-ui",
    ),
]
