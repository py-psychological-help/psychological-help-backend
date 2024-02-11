from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

from core.emails import (send_chat_url)
from chats.models import Chat

CustomUser = get_user_model()


@receiver(post_save, sender=Chat)
def sending_chat_to_client(sender, instance, created, **kwargs):
    """Отправляет ссылку клиенту."""
    if instance.psychologist and not instance.is_url_sent:
        send_chat_url(instance)
        instance.is_url_sent = True
        instance.save()