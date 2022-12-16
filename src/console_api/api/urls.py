from django.urls import include, path

urlpatterns = [
    path("feed/", include("api.feed.urls")),
    path("statistics/", include("api.statistics.urls")),
    path("source/", include("api.source.urls")),
    path("tag/", include("api.tag.urls")),
    path("", include("api.users.urls")),
    path("", include("api.system.urls"))
]
