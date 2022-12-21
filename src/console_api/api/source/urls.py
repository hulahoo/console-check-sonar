from rest_framework import routers

from api.source import views

router = routers.SimpleRouter()
router.register(r'source', views.SourceView)

urlpatterns = router.urls
