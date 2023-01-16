"""Urls for feed app"""

from django.urls import path
from rest_framework import routers

from console_api.feed.views import feed_add, feed_create, FeedListView, get_feed_preview, change_feed_properties_view

router = routers.SimpleRouter()
router.register(r'feeds', FeedListView)

urlpatterns = router.urls
urlpatterns += [
    # Create new feed
    path(
        '/feed-create/',
        feed_create,
        name="feed-create"),

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

    # GET request - get feed list
    # POST request - add feed
    path('', feed_add, name="feed-add|feed-get")
]
