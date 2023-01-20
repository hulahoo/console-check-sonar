"""Urls for feed app"""

from django.urls import path

from console_api.feed.views import (
    feed_preview_view,
    FeedView,
    update_feed_view,
)


urlpatterns = [
    # Feed preview
    path(
        "/feed-preview/",
        feed_preview_view,
        name="feed_preview",
    ),

    # Update feed
    path(
        "/<int:feed_id>",
        update_feed_view,
        name="change_properties",
    ),

    # Create feed and get feeds list
    path(
        "",
        FeedView.as_view(),
        name="feeds_view",
    ),
]
