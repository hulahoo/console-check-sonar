"""Urls for indicator app"""

from django.urls import path

from console_api.indicator.views import (
    add_comment_view,
    change_indicator_tags_view,
    IndicatorDetailView,
    IndicatorListView,
)


urlpatterns = [
    # Indicators list
    path(
        "",
        IndicatorListView.as_view(),
        name="indicator_list",
    ),

    # Change tags for the indicator
    path(
        "/<uuid:indicator_id>/change/tags",
        change_indicator_tags_view,
        name="indicator_change_tags",
    ),

    # Add action with add-comment type
    path(
        "/<uuid:indicator_id>/add-comment",
        add_comment_view,
        name="add_comment",
    ),

    # Indicator detail
    path(
        "/<uuid:id>",
        IndicatorDetailView.as_view(),
        name="indicator_detail",
    ),
]
