"""Urls for indicator app"""

from django.urls import path

from api.indicator.views import IndicatorStatiscList, IndicatorDetailView


urlpatterns = [
    path('', IndicatorStatiscList.as_view(), name='indicator_list'),
    path('<uuid:id>/', IndicatorDetailView.as_view(), name='indicator_detail'),
]
