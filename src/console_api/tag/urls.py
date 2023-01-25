"""Urls for tag app"""

from django.urls import path

from console_api.tag.views import DeleteTagView, TagsView


urlpatterns = [
    # Tags list
    path(
        "",
        TagsView.as_view(),
        name="tag_view",
    ),

    # Delete tag
    path(
        "/<int:tag_id>",
        DeleteTagView.as_view(),
        name="delete_tag",
    ),
]
