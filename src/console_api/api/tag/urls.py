from rest_framework import routers

from console_api.api.tag import views


router = routers.SimpleRouter()
router.register(r'tag', views.TagViewSet)

urlpatterns = router.urls
