from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save

from users.models import CustomClientUser

CustomUser = get_user_model()


def anonymize_data(sender, instance, **kwargs):
    """Маскирует текст символами '*' в именах, фамилиях, отчествах.

    Маскировка происходит только в том случае, если значение
    `settings.ANONYMIZE_DATA` установлено в True.
    """
    if not settings.ANONYMIZE_DATA:
        return
    for attr in ('first_name', 'last_name', 'patronymic'):
        value = getattr(instance, attr, None)
        if value:
            value = value[0].ljust(len(value), '*') if len(value) > 1 else '*'
            setattr(instance, attr, value)


pre_save.connect(anonymize_data,
                 sender=CustomUser,
                 dispatch_uid='CustomUser_anonymize')

pre_save.connect(anonymize_data,
                 sender=CustomClientUser,
                 dispatch_uid='CustomClientUser_anonymize')
