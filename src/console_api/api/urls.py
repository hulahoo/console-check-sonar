from django.urls import include, path

urlpatterns = [
    path("feed/", include("console_api.api.feed.urls")),
    path("statistics/", include("console_api.api.statistics.urls")),
    path("source/", include("console_api.api.source.urls")),
    path("tag/", include("console_api.api.tag.urls")),
    path("", include("console_api.api.users.urls")),
    
]
