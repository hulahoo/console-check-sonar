from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

swagger_title = "Console API"


schema_view = get_schema_view(
    openapi.Info(
        title=swagger_title,
        default_version="v1",
        description="Console API"
    ),
    patterns=[
        path("api/statistics/", include("console_api.api.statistics.urls")),
        path("api/", include("console_api.api.users.urls")),
    ],
)

statistics_api_schema_view = get_schema_view(
    openapi.Info(
        title=swagger_title,
        default_version="v1",
        description="Statistics API"
    ),
    patterns=[
        path("api/statistics/", include("console_api.api.statistics.urls")),
    ],
)

user_api_schema_view = get_schema_view(
    openapi.Info(
        title=swagger_title,
        default_version="v1",
        description="User API"
    ),
    patterns=[
        path("api/users/", include("console_api.api.users.urls")),
    ],
)

urlpatterns = [
    path(
        "api/doc/",
        schema_view.with_ui("swagger", cache_timeout=0),  # noqa
        name="schema-api-ui",
    )
]
