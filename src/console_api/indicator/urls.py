"""Urls for indicator app"""

from django.urls import path

from console_api.indicator.views import (
    add_comment_view,
    change_indicator_tags_view,
    indicator_detail_view,
    IndicatorListView,
    mark_indicator_as_false_positive_view,
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

    path(
        "/<uuid:indicator_id>/as_false_positive",
        mark_indicator_as_false_positive_view,
        name="indicator_as_false_positive",
    ),

    # Indicator detail or indicator deletion
    path(
        "/<uuid:indicator_id>",
        indicator_detail_view,
        name="indicator_detail",
    ),
]
