"""Project urls"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from console_api.system.views import (
    api_res,
    readiness_and_liveness_view,
    readiness_view,
    liveness_view,
    metrics_view,
)
from console_api.users.views import CustomAuthTokenView, DeleteAuthTokenView


schema_view = get_schema_view(
    openapi.Info(
        title="Console API",
        default_version="v3",
        description="Console API",
    ),
    patterns=[
        path("api/audit-logs", include("console_api.audit_logs.urls")),
        path("api/statistics/", include("console_api.statistics.urls")),
        path("api/users/", include("console_api.users.urls")),
        path("api/feeds", include("console_api.feed.urls")),
        path("api/source/", include("console_api.source.urls")),
        path("api/tag/", include("console_api.tag.urls")),
        path("api/detections/", include("console_api.detections.urls")),
        path("api/indicators/", include("console_api.indicator.urls")),
    ],
)

urlpatterns = [
    path("api/audit-logs", include("console_api.audit_logs.urls")),
    path("api/feeds", include("console_api.feed.urls")),
    path("api/statistics", include("console_api.statistics.urls")),
    path("api/source", include("console_api.source.urls")),
    path("api/tags", include("console_api.tag.urls")),
    path("api/users", include("console_api.users.urls")),
    path("api/detections", include("console_api.detections.urls")),
    path("api/sessions/<uuid:access_token>", DeleteAuthTokenView.as_view()),
    path("api/sessions", CustomAuthTokenView.as_view()),
    path("api/indicators", include("console_api.indicator.urls")),
    path(
        "api/doc",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-api-ui",
    ),
    path("health/liveness", liveness_view, name="liveness"),
    path("health/readiness", readiness_view, name="readiness"),
    path("health", readiness_and_liveness_view, name="readiness_and_liveness"),
    path("metrics", metrics_view, name="metrics"),
    path("api", api_res, name="api"),
    path("api/search", include("console_api.search.urls")),
    path("api/platform-settings", include("console_api.platform_settings.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))

    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
