"""Urls for feed app"""

from django.urls import path

from console_api.feed.views import (
    change_feed_properties_view,
    feeds_view,
    get_feed_preview,
)


urlpatterns = [
    # Get feed preview
    path(
        '/feed-preview/',
        get_feed_preview,
        name="feed-preview"),

    # Change feed properties
    path(
        '/<int:feed_id>',
        change_feed_properties_view,
        name="feed-change-properties",
    ),

    # /feeds GET and POST
    path(
        '',
        feeds_view,
        name="feeds_view",
    )
]
