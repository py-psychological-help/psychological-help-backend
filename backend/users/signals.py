from django.conf import settings
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from core.emails import (send_documents_confirm,
                         send_reg_confirm,
                         send_client_reg_confirm)
from users.models import CustomClientUser
from chats.models import Chat
from core.utils import create_secret_key

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


@receiver(post_save, sender=CustomClientUser)
def client_notification(sender, instance, created, **kwargs):
    """Отправляет уведомление о успешной регистрации."""
    if not instance.is_reg_confirm_sent:
        send_client_reg_confirm(instance)
        instance.is_reg_confirm_sent = True
        instance.save()


@receiver(post_save, sender=CustomClientUser)
def chat_auto_create(sender, instance, created, **kwargs):
    """Создает чат для нового клиента."""
    if not Chat.objects.filter(client=instance).exists():
        chat = Chat.objects.create(client=instance)
        create_secret_key(chat)
        chat.save()


@receiver(post_save, sender=CustomUser)
def psychologist_notification(sender, instance, created, **kwargs):
    """Отправляет уведомления о регистрации и проверке документов."""
    if instance.approved_by_moderator and not instance.is_approve_sent:
        send_documents_confirm(instance)
        instance.is_approve_sent = True
        instance.save()

    if not instance.is_reg_confirm_sent:
        instance.is_reg_confirm_sent = True
        instance.save()

    if instance.is_active:
        send_reg_confirm(instance)
