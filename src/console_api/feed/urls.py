"""Urls for feed app"""

from django.urls import path

from console_api.feed.views import (
    FeedPreview,
    FeedView,
    FeedUpdate,
    FeedsLastUpdateView,
    ProvidersListView,
    UpdateFeedsNowView,
)


urlpatterns = [
    # Update now
    path(
        "/update-now",
        UpdateFeedsNowView.as_view(),
        name="update_now",
    ),

    # Feed preview
    path(
        "/feed-preview",
        FeedPreview.as_view(),
        name="feed_preview",
    ),

    # Update feed or delete
    path(
        "/<int:feed_id>",
        FeedUpdate.as_view(),
        name="change_properties",
    ),

    # Providers list
    path(
        "/providers",
        ProvidersListView.as_view(),
        name="providers_list_view",
    ),

    # Create feed and get feeds list
    path(
        "",
        FeedView.as_view(),
        name="feeds_view",
    ),

    # Create feed and get feeds list
    path(
        "/last-update",
        FeedsLastUpdateView.as_view(),
        name="feeds_last_update",
    ),
]
