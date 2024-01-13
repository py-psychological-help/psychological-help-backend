from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from django.conf import settings
from chats.models import Chat

User = get_user_model()


class Command(BaseCommand):
    """Команда для тестов и отладки."""

    help = 'Import id command.'

    def handle(self, *args, **options):
        r = settings.REDIS
        chats = Chat.objects.all()
        for chat in chats:
            r.set(chat.chat_secret_key, chat.id)
            print(f'Ключ чата {chat.id} успешно импортирован в Redis')
