from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone

from .managers import CustomUserManager
from .validators import year_validator, birthday_validator


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Класс пользователей."""

    class Role(models.TextChoices):
        """Роли пользователей."""

        ADMIN = 'admin', 'Администратор'
        MODERATOR = 'moderator', 'Модератор'
        PSYCHOLOGIST = 'psychologist', 'Психолог'

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
        blank=False,
        verbose_name='Отчество'
    )
    role = models.CharField(
        max_length=25,
        choices=Role.choices,
        default='PSYCHOLOGIST'
    )
    photo = models.ImageField(
        upload_to='photos/', blank=True
    )
    email = models.EmailField('email адрес', blank=False, unique=True)
    birth_date = models.DateField(blank=True,
                                  null=True,
                                  validators=[birthday_validator, ])
    approved_by_moderator = models.BooleanField(blank=False, default=False)

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
    """Модель образования."""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Психолог',
        related_name='education'
    )
    university = models.CharField(
        'Название учебного заведения',
        max_length=100,
        blank=True
    )
    faculty = models.CharField(
        'Название факультета',
        max_length=100,
        blank=True
    )
    specialization = models.CharField(
        'Название специальности',
        max_length=100,
        blank=True
    )
    year_of_graduation = models.IntegerField('Год окончания',
                                             validators=[year_validator, ])

    scan = models.ImageField(
        upload_to='scans', blank=False
    )


class CustomClientUser(AbstractBaseUser):
    """Класс пользователей."""

    password = models.CharField('password', max_length=128, blank=True)

    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия'
    )
    patronymic = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Отчество'
    )

    photo = models.ImageField(
        upload_to='photos/', blank=True
    )
    email = models.EmailField('email адрес', blank=False, unique=True)
    birth_date = models.DateField(blank=True,
                                  null=True,
                                  validators=[birthday_validator, ])

    USERNAME_FIELD = "email"

    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)
