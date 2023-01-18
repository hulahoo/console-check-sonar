"""Urls for tag app"""

from django.urls import path

from console_api.tag.views import delete_tag_view, tags_view


urlpatterns = [
    # Tags list
    path(
        "",
        tags_view,
        name="tag_list",
    ),

    # Delete tag
    path(
        "/<int:tag_id>",
        delete_tag_view,
        name="delete_tag",
    ),
]
