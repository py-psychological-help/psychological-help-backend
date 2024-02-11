from django.apps import AppConfig
from django.conf import settings


class ChatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chats'

    def ready(self) -> None:
        import chats.signals
        from chats.models import Chat
        r = settings.REDIS
        chats = Chat.objects.all()
        for chat in chats:
            r.set(chat.chat_secret_key, chat.id)
            print(f'Ключ чата {chat.id} успешно импортирован в Redis')