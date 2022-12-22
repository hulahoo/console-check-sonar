from django.urls import path

from console_api.api.system.views import readiness, liveness, api_routes, metrics

urlpatterns = [
    path("health/liveness/", liveness, name="liveness"),
    path("health/readiness/", readiness, name="readiness"),
    path("api/", api_routes, name="api_routes"),
    path("metrics/", metrics, name="metrics"),
]
