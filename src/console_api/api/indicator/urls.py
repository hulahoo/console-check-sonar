"""Urls for indicator app"""

from django.urls import path

from console_api.api.indicator.views import (
    IndicatorDetailView,
    IndicatorListView,
)


urlpatterns = [
    # Indicators list
    path(
        "",
        IndicatorListView.as_view(),
        name="indicator_list",
    ),

    # Indicator detail
    path(
        "/<uuid:id>",
        IndicatorDetailView.as_view(),
        name="indicator_detail",
    ),
]
