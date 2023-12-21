from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField('Адрес электронной почты', max_length=254,
                              unique=True)
    username = models.CharField('Уникальный юзернейм', max_length=150,
                                unique=True)
    first_name = models.CharField('Имя', max_length=150, )
    last_name = models.CharField('Фамилия', max_length=150)
    password = models.CharField('Пароль', max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    class Meta:
        ordering = ['id', ]
        verbose_name = 'Пользователь'
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'username'],
                name='unique_user'
            )
        ]

    def __str__(self):
        return self.username
