"""Urls for statistics app"""

from django.urls import path

from console_api.api.statistics.views import (
    CheckedObjectsView,
    DetectedObjectsView,
    FeedsIntersectionList,
    FeedStatiscList,
    detected_indicators_view
)

urlpatterns = [
    path(
        "/feeds",
        FeedStatiscList.as_view(),
        name="feed_stat",
    ),
    path(
        "/matched-indicators",
        detected_indicators_view,
        name="matched_indicator",
    ),
    path(
        "/matched-objects",
        DetectedObjectsView.as_view(),
        name="matched_objects",
    ),
    path(
        "/checked-objects",
        CheckedObjectsView.as_view(),
        name="checked_objects",
    ),
    path(
        "/feeds-intersections",
        FeedsIntersectionList.as_view(),
        name="feeds_intersections",
    ),
]
