from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

swagger_title = "Console API"

# feed_api_schema_view = get_schema_view(
#     openapi.Info(
#         title=swagger_title,
#         default_version="v1",
#         description="Feed API"
#     ),
#     patterns=[
#         path("api/feed/", include("api.feed.urls")),
#     ],
# )

# indicator_api_schema_view = get_schema_view(
#     openapi.Info(
#         title=swagger_title,
#         default_version="v1",
#         description="Indicator API"
#     ),
#     patterns=[
#         path("api/indicator/", include("api.indicator.urls")),
#     ],
# )

schema_view = get_schema_view(
    openapi.Info(
        title=swagger_title,
        default_version="v1",
        description="Console API"
    ),
    patterns=[
        path("api/statistics/", include("api.statistics.urls")),
        path("api/users/", include("apps.users.urls")),
    ],
)

statistics_api_schema_view = get_schema_view(
    openapi.Info(
        title=swagger_title,
        default_version="v1",
        description="Statistics API"
    ),
    patterns=[
        path("api/statistics/", include("api.statistics.urls")),
    ],
)

user_api_schema_view = get_schema_view(
    openapi.Info(
        title=swagger_title,
        default_version="v1",
        description="User API"
    ),
    patterns=[
        path("api/users/", include("apps.users.urls")),
    ],
)

# source_api_schema_view = get_schema_view(
#     openapi.Info(
#         title=swagger_title,
#         default_version="v1",
#         description="Source API"
#     ),
#     patterns=[
#         path("api/source/", include("api.source.urls")),
#     ],
# )

# system_api_schema_view = get_schema_view(
#     openapi.Info(
#         title=swagger_title,
#         default_version="v1",
#         description="System API for healthcheck"
#     ),
#     patterns=[
#         path("api/", include("api.system.urls")),
#     ],
# )


urlpatterns = [
    # path(
    #     "docs/feed/",
    #     feed_api_schema_view.with_ui("swagger", cache_timeout=0),  # noqa
    #     name="schema-api-ui",
    # ),
    # path(
    #     "docs/indicator/",
    #     indicator_api_schema_view.with_ui("swagger", cache_timeout=0),  # noqa
    #     name="schema-api-ui",
    # ),
    # path(
    #     "docs/source/",
    #     source_api_schema_view.with_ui("swagger", cache_timeout=0),  # noqa
    #     name="schema-api-ui",
    # ),
    # path(
    #     "docs/api/",
    #     system_api_schema_view.with_ui("swagger", cache_timeout=0),  # noqa
    #     name="schema-api-ui",
    # ),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),  # noqa
        name="schema-api-ui",
    )
]
