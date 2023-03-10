"""Urls for users app"""

from django.urls import path

from console_api.users.views import UserView, UserDetail, UserChangePasswordView


urlpatterns = [
    path("", UserDetail.as_view(), name="user-create-get"),
    path("/<int:user_id>", UserView.as_view()),
    path("/change-password/<int:user_id>", UserChangePasswordView.as_view()),
]
