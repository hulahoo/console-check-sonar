from django.urls import path

from api.system.views import readiness, liveness

urlpatterns = [
    path("/health/liveness", liveness, name="liveness"),
    path("/health/readiness", readiness, name="readiness"),
]
