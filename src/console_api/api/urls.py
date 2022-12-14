from django.urls import include, path

urlpatterns = [
    path("feed/", include("api.feed.urls")),
    # path("", include("api.indicator.urls")),
    path("statistics/", include("api.statistics.urls")),
    path("source/", include("api.source.urls")),
    path("tag/", include("api.tag.urls")),
    path("", include("api.users.urls")),
    path("api/", include("api.system.urls"))
]
