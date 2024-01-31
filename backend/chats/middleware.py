from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware


@database_sync_to_async
def get_user(token):
    """Получение user по токену"""
    try:
        token_obj = Token.objects.get(key=token)
        return token_obj.user
    except Token.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
    """
    Промежуточное ПО для аутентификации пользователей
    на основе токена в строке запроса.
    """

    def __init__(self, inner):
        """Инициализация промежуточного ПО"""
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        """Метод обработки входящих запросов и аутентификации пользователей."""
        try:
            token_key = (
                dict((x.split('=') for x in scope['query_string'].
                      decode().split("&")))
            ).get('token', None)
        except ValueError:
            token_key = None
        user = AnonymousUser()
        if token_key:
            user = await get_user(token_key[:-1])
        scope['user'] = user
        return await super().__call__(scope, receive, send)
