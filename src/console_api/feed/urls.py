"""Urls for feed app"""

from django.urls import path

from console_api.feed.views import (
    feeds_view,
    get_feed_preview,
    update_feed_view,
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
        update_feed_view,
        name="change_properties",
    ),

    # /feeds GET and POST
    path(
        '',
        feeds_view,
        name="feeds_view",
    )
]
