from django.urls import include, path

from apps.users.views import CustomAuthTokenView


urlpatterns = [
    path("feeds", include("api.feed.urls")),
    # path("", include("api.indicator.urls")),
    path("statistics/", include("api.statistics.urls")),
    path("source/", include("api.source.urls")),
    path("tag/", include("api.tag.urls")),
    path("users", include("apps.users.urls")),
    path("api/", include("api.system.urls")),
    path("detections/", include("api.detections.urls")),
    path("sessions", CustomAuthTokenView.as_view()),
]
