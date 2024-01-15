import random
import string

from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

# from chat.models import Chat


def create_secret_key(chat):
    """Генерирует секретный ключ для чата."""
    later = string.ascii_letters + '0123456789'
    r = settings.REDIS
    length = settings.CHAT_SECRET_KEY_LENGTH
    while True:
        chat_secret_key = ''
        for i in range(length):
            chat_secret_key += random.choice(later)
        if not r.get(chat_secret_key):
            r.set(chat_secret_key, chat.id)
            chat.chat_secret_key = chat_secret_key
            chat.save()
            return chat_secret_key


def get_chat_id(chat_secret_key):
    """Получает chat_id по secret_key."""
    r = settings.REDIS
    return r.get(chat_secret_key)


def get_confirmation_code(user):
    """Генерирует ключ подтверждения почты."""
    return default_token_generator.make_token(user)
