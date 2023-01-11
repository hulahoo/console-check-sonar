"""Urls for statistics app"""

from django.urls import path

from console_api.statistics.views import (
    checked_objects_view,
    detected_objects_view,
    detected_indicators_view,
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
        detected_indicators_view,
        name="matched_indicator",
    ),
    path(
        "/matched-objects",
        detected_objects_view,
        name="matched_objects",
    ),
    path(
        "/checked-objects",
        checked_objects_view,
        name="checked_objects",
    ),
    path(
        "/feeds-intersections",
        FeedsIntersectionList.as_view(),
        name="feeds_intersections",
    ),
]
