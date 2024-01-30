import datetime
import json
from typing import Union

from asgiref.sync import sync_to_async
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework import mixins
from djangochannelsrestframework.observer.generics import (ObserverModelInstanceMixin, action)
from djangochannelsrestframework.observer import model_observer
from django.contrib.auth import get_user_model

from .models import Chat, Message

User = get_user_model()


class ChatConsumer(
    # ObserverModelInstanceMixin,
    GenericAsyncAPIConsumer):

    async def connect(self):
        await self.accept()
        self.chat_secret_key = self.scope['url_route']['kwargs']['chat_secret_key']
        self.chat = await self.get_chat()
        self.room_group_name = 'chat_%s' % self.chat_secret_key
        self.user = self.scope['user']

        error_message = await self.check_chat_access()

        if error_message:
            await self.send_error_message(error_message)
            await self.close()
            await super().disconnect(444)

        if self.user.is_anonymous:
            await self.set_connected_clients()
        else:
            await self.set_psy_in_chat()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        messages = await self.get_messages()
        await self.send_old_message(messages)

    async def receive(self, text_data):
        """Формируем словарь и отправляем через функцию уаказанную в type"""
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        await self.save_message(message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    async def chat_message(self, event):
        # Отправка сообщения обратно через WebSocket
        message = event['message']
        text = self.format_message(message=message, date=datetime.datetime.now())
        await self.send(text_data=text)
    

    async def disconnect(self, code):
        # if hasattr(self, "chat_subscribe"):
        #     await self.remove_user_from_room(self.chat_subscribe)
        #     await self.notify_users()
        if self.user.is_anonymous:
            await self.set_connected_clients(disconnected=True)
        await super().disconnect(code)

    
    @database_sync_to_async
    def get_messages(self):
        return list(Message.objects.filter(chat=self.chat).order_by('date_time'))[-2:]
    
    async def send_old_message(self, messages):
        """Печатаем все старые сообщения"""
        for message in messages:
            await self.send(
                self.format_message(
                    message=message.text,
                    date=message.date_time
                )
            )

    @database_sync_to_async
    def get_chat(self):
        """Получаем чат"""
        try:
            chat = Chat.objects.get(chat_secret_key=self.chat_secret_key)
        except Chat.DoesNotExist:
            return False
        return chat
    
    @database_sync_to_async
    def save_message(self, message):
        """Сохраняем сообщение в бд"""
        message = Message(chat=self.chat, text=message, is_psy_author=bool(self.user))
        message.save()

    @database_sync_to_async
    def set_psy_in_chat(self):
        """Записываем психолга в чат"""
        self.chat.psychologist = self.user
        self.chat.save()
    
    @database_sync_to_async
    def set_connected_clients(self, disconnected=False):
        """Добавляет в модель клиента при подключении и убирает при отключении"""
        if disconnected:
            self.chat.connected_clients -= 1
        else:
            self.chat.connected_clients += 1
        self.chat.save()

    async def check_chat_access(self):
        """Проверка на доступ к чату, возвращаем причину отказа или None"""
        if not self.chat:
            return '1 Чата не существует'
        if not self.chat.active:
            return '2 Чат завершен'
        if not self.user.is_anonymous and self.chat.psychologist_id and self.chat.psychologist_id != self.user.id:
            return '3 Психолог уже есть'
        if not self.user.is_anonymous and not self.user.approved_by_moderator:
            return '4 Дождитесь проверки документов'
        if self.user.is_anonymous and self.chat.connected_clients:
            return '5 В чате уже есть клиент'
    
    async def send_error_message(self, error_message):
        """Отправка текста ошибки"""
        await self.send(self.format_message(error_message))

    def format_message(self, error_message=None, message=None, date=None):
        data = {
            'error_msg': error_message,
            'message': message,
            'psy': not self.user.is_anonymous,
            'date': date.strftime('%Y-%m-%d %H:%M:%S') if date else date
        }
        return json.dumps(data)