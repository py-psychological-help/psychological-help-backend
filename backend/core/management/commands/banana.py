from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from django.conf import settings

from core.emails import (send_chat_url,)
from core.utils import create_secret_key
from chats.models import Chat


User = get_user_model()


class Command(BaseCommand):
    """Команда для тестов и отладки."""

    help = 'Test command.'

    def handle(self, *args, **options):
        r = settings.REDIS
        secret_key = create_secret_key()
        chat = Chat.objects.last()
        r.set(secret_key, chat.id)
        send_chat_url(chat)
