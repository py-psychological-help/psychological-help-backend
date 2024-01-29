from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from PIL import Image

from .managers import CustomUserManager
from .validators import (AlphanumericValidator,
                         birthday_validator,
                         EmailSymbolsValidator,
                         NameSpacesValidator,
                         NameSymbolsValidator)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Класс пользователей."""

    prefix = 'p'

    class Role(models.TextChoices):
        """Роли пользователей."""

        ADMIN = 'admin', 'Администратор'
        MODERATOR = 'moderator', 'Модератор'
        PSYCHOLOGIST = 'psychologist', 'Психолог'

    first_name = models.CharField(
        max_length=50,
        blank=False,
        verbose_name='Имя',
        validators=[NameSpacesValidator,
                    NameSymbolsValidator, ]
    )
    last_name = models.CharField(
        max_length=50,
        blank=False,
        verbose_name='Фамилия',
        validators=[NameSpacesValidator,
                    NameSymbolsValidator, ]
    )
    patronymic = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Отчество',
        validators=[NameSpacesValidator,
                    NameSymbolsValidator, ]
    )
    role = models.CharField(
        max_length=25,
        choices=Role.choices,
        default='PSYCHOLOGIST'
    )
    photo = models.ImageField(
        upload_to='photos/', blank=True
    )
    email = models.EmailField('email адрес',
                              blank=False,
                              unique=True,
                              max_length=50,
                              validators=[AlphanumericValidator,
                                          EmailSymbolsValidator])
    birth_date = models.DateField(blank=True,
                                  null=True,
                                  validators=[birthday_validator, ])
    approved_by_moderator = models.BooleanField('Подтверждение модератора',
                                                blank=False,
                                                default=False,)
    is_reg_confirm_sent = models.BooleanField('Письмо о рег-и направлено',
                                              default=False)
    is_approve_sent = models.BooleanField('Письмо о проверке док-в направлено',
                                          default=False)

    USERNAME_FIELD = "email"

    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text=('Designates whether the user can log into this admin '
                   'site.'))
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    confirmation_code = models.CharField(max_length=5, blank=True)
    greeting = models.TextField('Приветственное сообщение', blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return str(self.first_name + ' ' + self.last_name)

    class Meta:
        verbose_name = 'Психолог'
        verbose_name_plural = 'Психологи'


class Document(models.Model):
    """Модель документа."""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Психолог',
        related_name='document'
    )
    name = models.CharField(
        'Название документа',
        max_length=100,
        blank=True
    )

    scan = models.ImageField('Скан документа',
                             upload_to='scans',
                             blank=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """Сжимает загруженные сертификаты до нечитаемости."""
        super().save()
        if settings.COMPRESS_IMAGE:
            with Image.open(self.scan.path) as image:
                output_size = (60, 60)
                image.thumbnail(output_size)
                image.save(self.scan.path)

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


class CustomClientUser(AbstractBaseUser):
    """Модель клиентов."""

    prefix = 'c'
    password = models.CharField('password', max_length=20, blank=True,)

    first_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Имя',
        validators=[NameSpacesValidator,
                    NameSymbolsValidator, ])

    last_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Фамилия',
        validators=[NameSpacesValidator,
                    NameSymbolsValidator, ])

    patronymic = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Отчество',
        validators=[NameSpacesValidator,
                    NameSymbolsValidator, ])

    photo = models.ImageField(upload_to='photos/', blank=True)
    email = models.EmailField('email адрес',
                              blank=False,
                              unique=True,
                              validators=[AlphanumericValidator,
                                          EmailSymbolsValidator, ])
    birth_date = models.DateField(blank=True,
                                  null=True,
                                  validators=[birthday_validator, ])

    USERNAME_FIELD = "email"

    is_active = models.BooleanField(default=True)
    is_reg_confirm_sent = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()
    complaint = models.TextField(blank=False)

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
