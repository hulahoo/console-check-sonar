"""Main urls"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from console_api.api.system.views import (
    readiness_and_liveness_view, readiness_view, liveness_view, metrics_view, api_res
)


urlpatterns = [
    path("console-admin/", admin.site.urls),
    path("api/", include("console_api.api.urls")),
    path("health/liveness", liveness_view, name="liveness"),
    path("health/readiness", readiness_view, name="readiness"),
    path("health", readiness_and_liveness_view, name="readiness_and_liveness"),
    path("metrics", metrics_view, name="metrics"),
    path("host/api", api_res, name="api")
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
