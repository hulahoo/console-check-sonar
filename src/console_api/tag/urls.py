"""Urls for tag app"""

from django.urls import path

from console_api.tag.views import tags_view


urlpatterns = [
    # Tags list
    path(
        "",
        tags_view,
        name="tag_list",
    ),
]
