from PIL import Image
from pathlib import Path
from io import BytesIO

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.core.files import File


from .managers import CustomUserManager
from .validators import (AlphanumericValidator,
                         birthday_validator,
                         EmailSymbolsValidator,
                         NameSpacesValidator,
                         NameSymbolsValidator,
                         year_validator)


image_types = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "gif": "GIF",
    "tif": "TIFF",
    "tiff": "TIFF",
}


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
        blank=True
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
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    confirmation_code = models.CharField(max_length=5, blank=True)
    greeting = models.TextField('Приветственное сообщение', blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return str(self.first_name + ' ' + self.last_name)

    class Meta:
        verbose_name = 'Психолог'
        verbose_name_plural = 'Психологи'
        ordering = ('pk',)


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

    scan = models.ImageField(blank=False)

    def image_resize(self, width, height):
        image = self.scan
        with Image.open(image) as img:
            # check if either the width or height is greater than the max
            if (img.width > width or img.height > height
                    and settings.COMPRESS_IMAGE):
                output_size = (width, height)
                # Create a new resized “thumbnail” version of the image with P
                img.thumbnail(output_size)
                # Find the file name of the image
                img_filename = Path(image.file.name).name
                # Spilt the filename on “.” to get the file extension only
                img_suffix = Path(image.file.name).name.split(".")[-1]
                # Use the file extension to determine the file type from the
                # image_types dictionary
                img_format = image_types[img_suffix]
                # Save the resized image into the buffer, noting the correct f
                # ile type
                buffer = BytesIO()
                img.save(buffer, format=img_format)
                # Wrap the buffer in File object
                file_object = File(buffer)
                # Save the new resized file as usual, which will save to S3
                # using django-storages
                image.save(img_filename, file_object)

    def save(self, *args, **kwargs):
        # self.image_resize(60, 60)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


class CustomClientUser(AbstractBaseUser):
    """Модель клиентов."""

    prefix = 'c'
    password = models.CharField('password', max_length=128, blank=True)

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

    photo = models.ImageField('Фото', blank=True)
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
