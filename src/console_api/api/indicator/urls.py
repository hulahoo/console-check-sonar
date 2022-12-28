"""Urls for indicator app"""

from django.urls import path

from console_api.api.indicator.views import (
    IndicatorDetailView,
    IndicatorStatiscList,
)


urlpatterns = [
    # Indicators list
    path(
        "",
        IndicatorStatiscList.as_view(),
        name="indicator_list",
    ),

    # Indicator detail
    path(
        "/<uuid:id>/",
        IndicatorDetailView.as_view(),
        name="indicator_detail",
    ),
]
