"""Urls for feed app"""

from django.urls import path

from console_api.feed.views import (
    FeedPreview,
    FeedView,
    FeedUpdate,
)


urlpatterns = [
    # Feed preview
    path(
        "/feed-preview",
        FeedPreview.as_view(),
        name="feed_preview",
    ),

    # Update feed
    path(
        "/<int:feed_id>",
        FeedUpdate.as_view(),
        name="change_properties",
    ),

    # Create feed and get feeds list
    path(
        "",
        FeedView.as_view(),
        name="feeds_view",
    ),
]
