"""Urls for indicator app"""

from django.urls import path

from api.indicator.views import IndicatorStatiscList


urlpatterns = [
    path('indicators', IndicatorStatiscList.as_view(), name='indicator_stat'),
]
