"""Urls for indicator app"""

from django.urls import path

from console_api.api.indicator.views import (
    change_indicator_tags_view,
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

    # Change tags for the indicator
    path(
        "/<uuid:indicator_id>/change/tags",
        change_indicator_tags_view,
        name="indicator_change_tags",
    ),

    # Indicator detail
    path(
        "/<uuid:id>",
        IndicatorDetailView.as_view(),
        name="indicator_detail",
    ),
]
