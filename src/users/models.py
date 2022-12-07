from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager

from src.models.abstract import BaseModel


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    username = models.CharField(unique=True, max_length=255)

    @property
    def is_staff(self):
        return self.is_superuser

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []
