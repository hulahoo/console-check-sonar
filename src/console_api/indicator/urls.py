"""Urls for indicator app"""

from django.urls import path
from rest_framework.routers import DefaultRouter

from console_api.indicator.views import (
    IndicatorAddComment,
    ChangeIndicatorTags,
    IndicatorDetail,
    IndicatorView,
    IndicatorIsSendToDections,
    MarkIndicatorAsFalsePositiveView,
)

router = DefaultRouter()
router.register("", IndicatorView)


urlpatterns = [
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
    path(
        "/<uuid:indicator_id>/is_sending_to_detections",
        IndicatorIsSendToDections.as_view(),
        name="indicator_is_send_to_detecions",
    ),
]

urlpatterns += router.urls
