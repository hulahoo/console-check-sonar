"""Urls for statistics app"""

from django.urls import path

from console_api.api.statistics.views import (
    CheckedObjectsView,
    DetectedIndicatorsView,
    DetectedObjectsView,
    FeedsIntersectionList,
    FeedStatiscList,
)

urlpatterns = [
    path(
        "/feeds",
        FeedStatiscList.as_view(),
        name="feed_stat",
    ),
    path(
        "/matched-indicators",
        DetectedIndicatorsView.as_view(),
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
