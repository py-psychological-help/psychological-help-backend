from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


from django.conf import settings
from .validators import validate_username
from .managers import CustomUserManager
from django.utils import timezone


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Класс пользователей."""

    class Role(models.TextChoices):
        """Роли пользователей."""

        ADMIN = 'admin', 'Администратор'
        MODERATOR = 'moderator', 'Модератор'
        PSYCHOLOGIST = 'psychologist', 'Психолог'
        CLIENT = 'client', 'Клиент'

    first_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Фамилия'
    )
    patronymic = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Отчество'
    )
    role = models.CharField(
        max_length=25,
        choices=Role.choices,
    )
    photo = models.ImageField(
        upload_to='photos/', blank=True
    )
    approved_by_moderator = models.BooleanField(blank=False, default=False)
    email = models.EmailField('email адрес', blank=False, unique=True)

    USERNAME_FIELD = "email"

    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text=('Designates whether the user can log into this admin '
                   'site.'))
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)


class Education(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Психолог',
        related_name='education'
    )
