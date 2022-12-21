from django.urls import path

from api.users import views
from apps.users.views import RegisterUserAPIView, Logout


urlpatterns = [
    path("/", RegisterUserAPIView.as_view()),
    path('logout', views.Logout.as_view()),
]
