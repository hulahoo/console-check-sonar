from django.urls import path
from rest_framework.authtoken import views as views_auth

from console_api.api.users import views


urlpatterns = [
    # path('register/', views.RegisterUserAPIView.as_view()),
    path('sessions/', views_auth.obtain_auth_token),
    path('logout/', views.Logout.as_view()),
]
