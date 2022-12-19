from django.urls import include, path

from rest_framework.authtoken import views as views_auth


urlpatterns = [
    path("feed/", include("api.feed.urls")),
    # path("", include("api.indicator.urls")),
    path("statistics/", include("api.statistics.urls")),
    path("source/", include("api.source.urls")),
    path("tag/", include("api.tag.urls")),
    path("users", include("apps.users.urls")),
    path("api/", include("api.system.urls")),
    path('sessions', views_auth.obtain_auth_token),
]
