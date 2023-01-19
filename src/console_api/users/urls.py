"""Urls for users app"""

from django.urls import path

from console_api.users.views import user_detail_view, users_view, Logout


urlpatterns = [
    path("", users_view),
    path("/<int:user_id>", user_detail_view),
    path('/logout', Logout.as_view()),
]
