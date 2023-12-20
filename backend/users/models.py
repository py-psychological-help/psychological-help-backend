from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import PROTECT #лишнее

from validators import validate_username


class Education(models.Model):
    pass


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
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    photo = models.ImageField(
        upload_to='photos/'
    )
    approved_by_moderator = models.BooleanField(blank=True)
    education = models.ForeignKey(
        Education,
        on_delete=PROTECT, # зачем ПРОТЕКТ? удаляем узера - пускай удаляется и образорвание: models.CASCAD
        blank=True
    )
