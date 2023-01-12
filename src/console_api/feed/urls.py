"""Urls for feed app"""

from django.urls import path
from rest_framework import routers

from console_api.feed.views import feed_add, feed_create, FeedListView, get_feed_preview

router = routers.SimpleRouter()
router.register(r'feeds', FeedListView)

urlpatterns = router.urls
urlpatterns += [
    path('/feed-create/', feed_create, name="feed-create"),
    path('/feed-preview/', get_feed_preview, name="feed-preview"),
    path("", feed_add, name="feed-add|feed-get"),
]
