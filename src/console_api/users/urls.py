"""Urls for users app"""

from django.urls import path

from console_api.users.views import RegisterUserAPIView, Logout


urlpatterns = [
    path("/", RegisterUserAPIView.as_view()),
    path('logout', Logout.as_view()),
]
