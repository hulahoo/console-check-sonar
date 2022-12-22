from django.urls import path

from console_api.api.statistics.views import (
    FeedStatiscList, MatchedIndicatorStatiscList,
    MatchedObjectsStatiscList, CheckedObjectsStatiscList, FeedsIntersectionList
)

urlpatterns = [
    path('feeds', FeedStatiscList.as_view(), name='feed_stat'),
    path('matched-indicators', MatchedIndicatorStatiscList.as_view(), name='indicator_matched'),
    path('matched-objects', MatchedObjectsStatiscList.as_view(), name='objects_matched'),
    path('checked-objects', CheckedObjectsStatiscList.as_view(), name='objects_checked'),
    path('feeds-intersections', FeedsIntersectionList.as_view(), name="feeds_intersections"),
]
