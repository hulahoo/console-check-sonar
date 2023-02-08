"""Urls for indicator app"""

from django.urls import path
from rest_framework.routers import DefaultRouter

from console_api.indicator.views import (
    ChangeIndicatorTagsView,
    IndicatorAddComment,
    IndicatorDetailView,
    IndicatorsView,
    IndicatorIsSendingToDetectionsView,
    MarkIndicatorAsFalsePositiveView,
    MarkListAsNotFalsePositiveView,
    ScoreIndicatorsView
)

router = DefaultRouter()
router.register("", IndicatorsView)


urlpatterns = [
    # Change tags for the indicator
    path(
        "/<uuid:indicator_id>/change/tags",
        ChangeIndicatorTagsView.as_view(),
        name="indicator_change_tags",
    ),

    # Add action with add-comment type
    path(
        "/<uuid:indicator_id>/add-comment",
        IndicatorAddComment.as_view(),
        name="add_comment",
    ),

    # Mark as_false_positive
    path(
        "/<uuid:indicator_id>/as-false-positive",
        MarkIndicatorAsFalsePositiveView.as_view(),
        name="indicator_as_false_positive",
    ),

    # Indicator detail or indicator deletion
    path(
        "/<uuid:indicator_id>",
        IndicatorDetailView.as_view(),
        name="indicator_detail",
    ),

    # Indicator is_sending_to_detections
    path(
        "/<uuid:indicator_id>/is-sending-to-detections",
        IndicatorIsSendingToDetectionsView.as_view(),
        name="indicator_is_send_to_detecions",
    ),

    # Mark list of indicators as false positive
    path(
        "/list-as-not-false-positive",
        MarkListAsNotFalsePositiveView.as_view(),
        name="list_as_not_false_positive",
    ),
    path(
        "/update-now",
        ScoreIndicatorsView.as_view(),
        name="update-indicators"
    )
]

urlpatterns += router.urls
