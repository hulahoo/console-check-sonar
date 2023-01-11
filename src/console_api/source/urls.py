"""Urls for source app"""

from rest_framework import routers

from console_api.source import views


router = routers.SimpleRouter()
router.register(r'source', views.SourceView)

urlpatterns = router.urls
