from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

swagger_title = "Console API"

feed_api_schema_view = get_schema_view(
    openapi.Info(
        title=swagger_title,
        default_version="v1",
        description="Feed API"
    ),
    public=False,
    patterns=[
        path("api/feed/", include("api.feed.urls")),
    ],
)

indicator_api_schema_view = get_schema_view(
    openapi.Info(
        title=swagger_title,
        default_version="v1",
        description="Indicator API"
    ),
    public=False,
    patterns=[
        path("api/indicator/", include("api.indicator.urls")),
    ],
)

source_api_schema_view = get_schema_view(
    openapi.Info(
        title=swagger_title,
        default_version="v1",
        description="Source API"
    ),
    public=False,
    patterns=[
        path("api/source/", include("api.source.urls")),
    ],
)

urlpatterns = [
    path(
        "docs/feed/",
        feed_api_schema_view.with_ui("swagger", cache_timeout=0),  # noqa
        name="schema-api-ui",
    ),
    path(
        "docs/indicator/",
        indicator_api_schema_view.with_ui("swagger", cache_timeout=0),  # noqa
        name="schema-api-ui",
    ),
    path(
        "docs/source/",
        source_api_schema_view.with_ui("swagger", cache_timeout=0),  # noqa
        name="schema-api-ui",
    ),
]
