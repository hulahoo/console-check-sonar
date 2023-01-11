"""Urls for tag app"""

from rest_framework import routers

from console_api.tag import views


router = routers.SimpleRouter()
router.register(r'tag', views.TagViewSet)

urlpatterns = router.urls
