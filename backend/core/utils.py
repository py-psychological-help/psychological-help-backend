import random
import string

from django.contrib.auth.tokens import default_token_generator

# from chat.models import Chat


def create_secret_key(length=10):
    """Генерирует секретный ключ для чата."""
    later = string.ascii_letters + '0123456789'
    while True:
        id = ''
        for i in range(length):
            id += random.choice(later)
        # if not Chat.objects.filter(chat_secret_key=id).exists():
        if True:
            return id


def get_confirmation_code(user):
    """Генерирует ключ подтверждения почты."""
    return default_token_generator.make_token(user)


def get_confirmation_code(user):
    return default_token_generator.make_token(user)
