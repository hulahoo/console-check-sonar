from django.urls import path

from console_api.api.users import views
from console_api.apps.users.views import RegisterUserAPIView


urlpatterns = [
    path("/", RegisterUserAPIView.as_view()),
    path('logout', views.Logout.as_view()),
]
