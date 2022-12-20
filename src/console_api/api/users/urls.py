from django.urls import path
from rest_framework.authtoken import views as views_auth

from api.users import views


urlpatterns = [
    path('sessions/', views_auth.obtain_auth_token),
    path('logout/', views.Logout.as_view()),
]
