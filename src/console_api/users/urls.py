"""Urls for users app"""

from django.urls import path

from console_api.users.views import (
    change_user_password_view,
    users_view,
    Logout,
)


urlpatterns = [
    path("", users_view),
    path("/<int:user_id>", change_user_password_view),
    path('/logout', Logout.as_view()),
]
