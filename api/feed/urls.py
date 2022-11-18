from django.urls import path
from rest_framework import routers

from api.feed import views

router = routers.SimpleRouter()
router.register(r'feeds', views.FeedListView)

urlpatterns = router.urls
urlpatterns += [
    path("new/", views.feed_add, name="feed_add"),
    path('feed_create/', views.feed_create, name="feed_create"),
]
