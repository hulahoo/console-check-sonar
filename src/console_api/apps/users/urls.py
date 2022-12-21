from django.urls import path
# from rest_framework import routers

from .views import RegisterUserAPIView, Logout


urlpatterns = [
    path("/", RegisterUserAPIView.as_view()),
    path('logout/', Logout.as_view()),
]
