from django.urls import path
# from rest_framework import routers
from rest_framework.authtoken import views as views_auth

from api.users import views

# router = routers.SimpleRouter()
# router.register(r'users', views.UserViewSet)

# urlpatterns = router.urls

urlpatterns = [
    path('register/', views.RegisterUserAPIView.as_view()),
    path('sessions/', views_auth.obtain_auth_token),
    path('logout/', views.Logout.as_view()),
]
