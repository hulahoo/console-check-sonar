from django.urls import path
from rest_framework import routers

from api.feed.views import feed_add, feed_create, FeedListView

router = routers.SimpleRouter()
router.register(r'feeds', FeedListView)

urlpatterns = router.urls
urlpatterns += [
    path("/", feed_add, name="feed_add"),
    path('feed_create/', feed_create, name="feed_create"),
]
