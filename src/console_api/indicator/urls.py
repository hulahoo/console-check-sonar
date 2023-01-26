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
        "/<uuid:indicator_id>/as_false_positive",
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
        "/<uuid:indicator_id>/is_sending_to_detections",
        IndicatorIsSendingToDetectionsView.as_view(),
        name="indicator_is_send_to_detecions",
    ),
]

urlpatterns += router.urls
