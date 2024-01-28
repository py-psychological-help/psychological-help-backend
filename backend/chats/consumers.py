import datetime
import json

from asgiref.sync import sync_to_async
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework import mixins
from djangochannelsrestframework.observer.generics import (ObserverModelInstanceMixin, action)
from djangochannelsrestframework.observer import model_observer
from django.contrib.auth import get_user_model

from .models import Chat, Message
from api.serializers import MessageSerializer, ChatSerializer, UserSerializer

User = get_user_model()


class ChatConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = Chat.objects.all()
    serializer_class = MessageSerializer
    lookup_field = "pk"
    # all_messages = []

    async def connect(self):
        await self.accept()
        chat_secret_key = self.scope['url_route']['kwargs']['chat_secret_key']
        chat = await self.get_chat(chat_secret_key)
        self.chat= chat
        self.room_group_name = 'chat_%s' % chat_secret_key
        if await self.check_chat_access(chat):
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            messages = await self.get_message(chat)
            await self.send_old_message(messages)
        else:
            await self.send_error_message('чат не найден')
            await self.close()

    async def receive(self, text_data):
            """Формируем словарь и отправляем через функцию уаказанную в type"""
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            token = self.scope['query_string'].split(b'=')[1].decode()[:-1] # получение токена из url
            user = await self.get_user(token)
            
            await self.save_message(message, user)
 
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': 'psy' if user else 'anon',
                    'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            )

    async def chat_message(self, event):
        # Отправка сообщения обратно через WebSocket
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': event['sender'],
            'date': event['date']
        }))

    async def disconnect(self, code):
        if hasattr(self, "chat_subscribe"):
            await self.remove_user_from_room(self.chat_subscribe)
            await self.notify_users()
        await super().disconnect(code)


    @database_sync_to_async
    def get_user(self, token):
        """Получаем юзера через токен"""
        try:
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
        except Token.DoesNotExist:
            user = None
        return user
    
    @database_sync_to_async
    def get_message(self, chat):
        return list(Message.objects.filter(chat=chat))
    
    async def send_old_message(self, messages):
        for message in messages:
            await self.send(text_data=json.dumps({
                'message': message.text,
                'sender': 'psy' if message.is_psy_author else 'anon',
                'date': message.date_time.strftime('%Y-%m-%d %H:%M:%S')
            }))

    @database_sync_to_async
    def get_chat(self, chat_secret_key):
        try:
            chat = Chat.objects.get(chat_secret_key=chat_secret_key)
        except Chat.DoesNotExist:
            return False
        return chat
    
    @database_sync_to_async
    def save_message(self, message, user):
        message = Message(chat=self.chat, text=message, is_psy_author=bool(user))
        message.save()

    @database_sync_to_async
    def check_chat_access(self, chat):
        return True
        try:
            chat = Chat.objects.get(chat_secret_key=self.chat_secret_key)
        except Chat.DoesNotExist:
            return False
        return chat

    
    async def send_error_message(self, error_message):
        await self.send(text_data=json.dumps({
            'error': error_message
        }))


class UserConsumer(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.PatchModelMixin,
        mixins.UpdateModelMixin,
        mixins.CreateModelMixin,
        mixins.DeleteModelMixin,
        GenericAsyncAPIConsumer,
):

    queryset = User.objects.all()
    serializer_class = UserSerializer