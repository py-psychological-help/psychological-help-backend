from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from core.emails import (send_education_confirm, send_reg_confirm,
                         send_chat_url, send_confirmation_code)

from django.conf import settings
from core.utils import create_secret_key, get_confirmation_code

User = get_user_model()


class Command(BaseCommand):
    """Команда для тестов и отладки."""

    help = 'Test command.'

    def handle(self, *args, **options):
        user = User.objects.first()
        send_education_confirm(user)
        # send_reg_confirm(user)
        # chat_url = (settings.ALLOWED_HOSTS[-1]
        #             + '/chats/'
        #             + create_secret_key(40))
        # send_chat_url(user, chat_url)
        # send_confirmation_code(user, get_confirmation_code(user))
