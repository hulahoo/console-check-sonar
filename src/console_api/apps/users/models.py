"""Models for users app"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


USER_ROLES = (
    ("analyst", "analyst"),
    ("admin", "admin"),
    ("auditor", "auditor"),
)


class UserManager(BaseUserManager):
    """Manager for User model"""

    def create_user(self, login: str, password: str = None, **extra_fields):
        """Create and save user with the given login and password"""

        user = self.model(login=login, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_staffuser(self, login: str, password: str, **extra_fields):
        """Create and save a staff user with the given login and password"""

        user = self.create_user(
            login=login,
            password=password,
            **extra_fields,
        )

        user.staff = True
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

    login = models.TextField(
        "Логин",
        unique=True,
    )

    password = models.TextField(
        "Хэшированный пароль",
        db_column="pass_hash",
    )

    full_name = models.TextField(
        "Полное имя",
    )

    role = models.TextField(
        "Роль",
        choices=USER_ROLES,
    )

    is_active = models.BooleanField(
        "Есть ли у пользователя доступ к системе (не отключен ли он?)",
        default=True,
    )

    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        verbose_name="ID Пользователя, кто создал этого Пользователя",
        null=True,
        blank=True,
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

    staff = models.BooleanField(
        "Персонал?",
        default=False
    )

    admin = models.BooleanField(
        "Админ?",
        default=False
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

    @property
    def is_staff(self) -> bool:
        """Is the staff user?"""

        return self.staff

    @property
    def is_admin(self) -> bool:
        """Is the admin user?"""

        return self.admin

    class Meta:
        """Metainformation about the model"""

        db_table = "users"
