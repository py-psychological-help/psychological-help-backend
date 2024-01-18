from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from PIL import Image


from core.emails import (send_education_confirm,
                         send_reg_confirm,
                         send_client_reg_confirm)
from .managers import CustomUserManager
from .validators import year_validator, birthday_validator


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Класс пользователей."""

    prefix = 'p'

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
        blank=True,
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
    is_reg_confirm_sent = models.BooleanField(default=False)
    is_approve_sent = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text=('Designates whether the user can log into this admin '
                   'site.'))
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    confirmation_code = models.CharField(max_length=5, blank=True)
    greeting = models.TextField(blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return str(self.first_name + ' ' + self.last_name)


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
                                             validators=[year_validator, ],
                                             blank=True,
                                             null=True)

    scan = models.ImageField(
        upload_to='scans', blank=False
    )

    def save(self):
        """Сжимает загруженные сертификаты до нечитаемости."""
        super().save()
        if settings.COMPRESS_IMAGE:
            with Image.open(self.scan.path) as image:
                output_size = (60, 60)
                image.thumbnail(output_size)
                image.save(self.scan.path)


class CustomClientUser(AbstractBaseUser):
    """Модель клиентов."""

    id = models.AutoField(primary_key=True)
    prefix = 'c'
    password = models.CharField('password', max_length=128, blank=True)

    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя')

    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия')

    patronymic = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Отчество')

    photo = models.ImageField(upload_to='photos/', blank=True)
    email = models.EmailField('email адрес', blank=False, unique=True)
    birth_date = models.DateField(blank=True,
                                  null=True,
                                  validators=[birthday_validator, ])

    USERNAME_FIELD = "email"

    is_active = models.BooleanField(default=True)
    is_reg_confirm_sent = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()
    complaint = models.TextField(blank=True)

    def __str__(self):
        return self.prefix + str(self.id)


@receiver(post_save, sender=CustomUser)
def psychologist_notification(sender, instance, created, **kwargs):
    """Отправляет уведомления о регистрации и проверке документов."""
    if instance.approved_by_moderator and not instance.is_approve_sent:
        send_education_confirm(instance)
        instance.is_approve_sent = True
        instance.save()

    if not instance.is_reg_confirm_sent:
        send_reg_confirm(instance)
        instance.is_reg_confirm_sent = True
        instance.save()


@receiver(post_save, sender=CustomClientUser)
def client_notification(sender, instance, created, **kwargs):
    """Отправляет уведомление о успешной регистрации."""
    if not instance.is_reg_confirm_sent:
        send_client_reg_confirm(instance)
        instance.is_reg_confirm_sent = True
        instance.save()
