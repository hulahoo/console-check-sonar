from django.urls import include, path

urlpatterns = [
    path("feed/", include("api.feed.urls")),
    path("indicator/", include("api.indicator.urls")),
    path("source/", include("api.source.urls")),
]
