from django.urls import path

from . import consumers


websocket_urlpatterns = [
    path('ws/chat/<str:chat_secret_key>/', consumers.ChatConsumer.as_asgi()),
    path('ws/general_chat/', consumers.GeneralChatConsumer.as_asgi()),
]
