from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from console_api.apps.models.abstract import BaseModel


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    username = models.CharField(unique=True, max_length=255)

    @property
    def is_staff(self):
        return self.is_superuser

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
