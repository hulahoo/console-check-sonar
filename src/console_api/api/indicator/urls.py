from django.urls import path
from rest_framework import routers

from api.indicator import views


urlpatterns = [
    path('', views.IndicatorView.as_view(), name='indicator_list'),
    path('<str:uuid>/', views.IndicatorDetailView.as_view(), name='indicator_detail'),



    path(r'feeds', views.FeedStatiscList.as_view(), name='feed_stat'),
    path(r'indicators', views.IndicatorStatiscList.as_view(), name='indicator_stat'),
    path(r'matched-indicators', views.MatchedIndicatorStatiscList.as_view(), name='indicator_matched'),
    path(r'matched-objects', views.MatchedObjectsStatiscList.as_view(), name='objects_matched'),
    path(r'checked-objects', views.CheckedObjectsStatiscList.as_view(), name='objects_checked'),
    path(r'feeds-intersections', views.FeedsIntersectionList.as_view(), name="feeds_intersections"),
]
