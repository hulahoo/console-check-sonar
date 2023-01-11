"""Models for users app"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    """Manager for User model"""

    def create_user(self, login: str, password: str = None, **extra_fields):
        """Create and save user with the given login and password"""

        user = self.model(login=login, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, login: str, password: str, **extra_fields):
        """Create and save a superuser with the given login and password"""

        user = self.create_user(
            login=login,
            password=password,
            **extra_fields,
        )

        user.staff = True
        user.admin = True
        user.role = "admin"
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    """User model"""

    objects = UserManager()

    login = models.CharField(
        "Логин",
        max_length=128,
        unique=True,
    )

    password = models.CharField(
        "Хэшированный пароль",
        max_length=256,
        db_column="pass_hash",
    )

    full_name = models.CharField(
        "Полное имя",
        max_length=128,
    )

    role = models.CharField(
        "Роль",
        max_length=128,
    )

    is_active = models.BooleanField(
        "Есть ли у пользователя доступ к системе (не отключен ли он?)",
        default=True,
    )

    created_by = models.BigIntegerField(
        null=True,
        db_column="created_by",
    )

    created_at = models.DateTimeField(
        "Дата и время создания Пользователя",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "Дата и время обновления Пользователя",
        auto_now=True,
    )

    deleted_at = models.DateTimeField(
        "Дата и время удаления Пользователя",
        null=True,
        blank=True,
        editable=False,
    )

    USERNAME_FIELD = 'login'

    # Login & Password are required by default
    REQUIRED_FIELDS = []

    def get_full_name(self) -> str:
        return self.full_name

    def get_short_name(self) -> str:
        return self.login

    def __str__(self) -> str:
        return self.login

    def has_perm(self, perm, obj=None) -> bool:
        """Does the user have a specific permission?"""

        return self.is_active

    def has_module_perms(self, app_label) -> bool:
        """Does the user have permissions to view the app `app_label`?"""

        return self.is_active

    class Meta:
        """Metainformation about the model"""

        db_table = "users"


class Token(models.Model):
    """Token for authentication"""

    key = models.CharField(
        "Key",
        max_length=40,
        primary_key=True,
    )

    user = models.OneToOneField(
        "User",
        related_name='auth_token',
        on_delete=models.CASCADE,
        verbose_name="User",
    )

    created_at = models.DateTimeField(
        "Created",
        auto_now_add=True,
    )

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.key

    class Meta:
        """Metainformation for the model"""

        db_table = "token"
