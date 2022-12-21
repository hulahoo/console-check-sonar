from django.urls import path

from .views import RegisterUserAPIView, Logout


urlpatterns = [
    path("/", RegisterUserAPIView.as_view()),
    path('logout/', Logout.as_view()),
]
