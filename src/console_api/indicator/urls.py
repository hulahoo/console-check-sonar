"""Urls for indicator app"""

from django.urls import path

from console_api.indicator.views import (
    IndicatorAddComment,
    ChangeIndicatorTags,
    IndicatorDetail,
    IndicatorListView,
    MarkIndicatorAsFalsePositiveView,
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
        ChangeIndicatorTags.as_view(),
        name="indicator_change_tags",
    ),

    # Add action with add-comment type
    path(
        "/<uuid:indicator_id>/add-comment",
        IndicatorAddComment.as_view(),
        name="add_comment",
    ),

    path(
        "/<uuid:indicator_id>/as_false_positive",
        MarkIndicatorAsFalsePositiveView.as_view(),
        name="indicator_as_false_positive",
    ),

    # Indicator detail or indicator deletion
    path(
        "/<uuid:indicator_id>",
        IndicatorDetail.as_view(),
        name="indicator_detail",
    ),
]
