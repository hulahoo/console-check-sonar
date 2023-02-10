"""Urls for tag app"""

from django.urls import path

from console_api.tag.views import DeleteOrUpdateTagView, TagsView


urlpatterns = [
    # Tags list and create
    path(
        "",
        TagsView.as_view(),
        name="tag_list_create",
    ),

    # Delete or Update tag
    path(
        "/<int:tag_id>",
        DeleteOrUpdateTagView.as_view(),
        name="delete_or_update_tag",
    ),
]
