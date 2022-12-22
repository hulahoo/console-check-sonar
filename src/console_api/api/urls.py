from django.urls import include, path

from console_api.apps.users.views import CustomAuthTokenView


urlpatterns = [
    path("feeds", include("console_api.api.feed.urls")),
    # path("", include("api.indicator.urls")),
    path("statistics/", include("console_api.api.statistics.urls")),
    path("source/", include("console_api.api.source.urls")),
    path("tag/", include("console_api.api.tag.urls")),
    path("users", include("console_api.apps.users.urls")),
    path("api/", include("console_api.api.system.urls")),
    path("detections/", include("src.console_api.api.detections.urls")),
    path("sessions", CustomAuthTokenView.as_view()),
    path("indicators/", include("console_api.api.indicator.urls")),
]
