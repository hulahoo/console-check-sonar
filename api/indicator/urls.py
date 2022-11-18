from rest_framework import routers

from api.indicator import views

router = routers.SimpleRouter()
router.register(r'dashboard', views.Dashboard)
router.register(r'indicators', views.IndicatorListView)

urlpatterns = router.urls
