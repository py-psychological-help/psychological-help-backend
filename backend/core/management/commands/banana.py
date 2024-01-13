from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from core.emails import (send_education_confirm, send_reg_confirm,
                         send_chat_url, send_confirmation_code)

from django.conf import settings
from core.utils import create_secret_key, get_confirmation_code
from chats.models import Chat

User = get_user_model()


class Command(BaseCommand):
    """Команда для тестов и отладки."""

    help = 'Test command.'

    def handle(self, *args, **options):
        r = settings.REDIS
        # r.set("django-insecure-%x%lg4mv5ud25q@9v*&sq3k7&usb8ya@#i12+o*2+t+e31$4t5", "id 161654484")
        # res = r.get("django-insecure-%x%lg4mv5ud25q@9v*&sq3k7&usb8ya@#i12+o*2+t+e31$4t5")
        secret_key = create_secret_key()
        chat = Chat.objects.last()
        r.set(secret_key, chat.id)
        res = r.get(secret_key)
        print(secret_key)
        print(res)
        send_chat_url(chat)
