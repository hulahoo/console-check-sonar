from rest_framework import routers

from api.users import views


router = routers.SimpleRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = router.urls
