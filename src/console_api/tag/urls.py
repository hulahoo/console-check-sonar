"""Urls for tag app"""

from django.urls import path

from console_api.tag.views import TagsView, DeleteTag


urlpatterns = [
    # Tags list
    path(
        "",
        TagsView.as_view(),
        name="tag_list",
    ),

    # Delete tag
    path(
        "/<int:tag_id>",
        DeleteTag.as_view(),
        name="delete_tag",
    ),
]
