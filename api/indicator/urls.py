from django.urls import path
from rest_framework import routers

from api.indicator import views


urlpatterns = [
    path(r'statistics/feeds', views.FeedStatiscList.as_view(), name='feed_stat'),
    path(r'statistics/indicators', views.IndicatorStatiscList.as_view(), name='indicator_stat'),
    path(r'statistics/matched-objects', views.MatchedIndicatorStatiscList.as_view(), name='indicator_matched'),
]
