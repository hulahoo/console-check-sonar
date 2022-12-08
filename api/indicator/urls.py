from django.urls import path
from rest_framework import routers

from api.indicator import views


urlpatterns = [
    path(r'statistics/feeds', views.FeedStatiscList.as_view(), name='feed_stat'),
    path(r'statistics/indicators', views.IndicatorStatiscList.as_view(), name='indicator_stat'),
    path(r'statistics/matched-indicators', views.MatchedIndicatorStatiscList.as_view(), name='indicator_matched'),
    path(r'statistics/matched-objects', views.MatchedObjectsStatiscList.as_view(), name='objects_matched'),
    path(r'statistics/checked-objects', views.CheckedObjectsStatiscList.as_view(), name='objects_checked'),
    path(r'statistics/feeds-intersections', views.FeedStatiscList.as_view(), name="feeds_intersections"),
]
