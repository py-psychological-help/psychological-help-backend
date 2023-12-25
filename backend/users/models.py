from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import validate_username


class User(AbstractUser):
    username = models.CharField(
        max_length=20,
        unique=True,
        help_text='Обязательное поле. 5-15 символов.'
                  'Разрешены только буквы, цифры и знаки -/_',
        error_messages={
            'unique': "Пользователь с таким логином уже существует.",
        },
        validators=[
            MinLengthValidator(5, 'Минимум 5 символов'),
            validate_username,
        ]
    )
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
    photo = models.ImageField(
        upload_to='photos/'
    )
    approved_by_moderator = models.BooleanField(blank=True)


class Education(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Психолог',
        related_name='education'
    )
