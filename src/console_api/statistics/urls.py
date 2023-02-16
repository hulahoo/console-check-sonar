"""Urls for statistics app"""

from django.urls import path

from console_api.statistics.views import (
    checked_objects_view,
    detected_objects_view,
    detected_indicators_view,
    FeedsIntersectionView,
    FeedsStatisticView,
    FeedForceUpdateStatistics,
    indicators_statistic_view,
)


urlpatterns = [
    path(
        "/feeds",
        FeedsStatisticView.as_view(),
        name="feeds_stat",
    ),
    path(
        "/indicators",
        indicators_statistic_view,
        name="indicators_stat",
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
        FeedsIntersectionView.as_view(),
        name="feeds_intersections",
    ),
    path(
        "/feeds-force-update",
        FeedForceUpdateStatistics.as_view(),
        name="feeds-force-update-statistics",
    ),

]
