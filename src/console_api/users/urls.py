"""Urls for users app"""

from django.urls import path

from console_api.users.views import users_view, Logout


urlpatterns = [
    path("", users_view),
    path('logout', Logout.as_view()),
]
