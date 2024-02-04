import json

from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from channels.db import database_sync_to_async

from .models import Chat, Message


class ChatConsumer(GenericAsyncAPIConsumer):

    async def connect(self):
        """
        Отрабатывает при коннекте

        достаем данные и проверяем на доступность
        если доступ не проходит выводим сообщение на фронт и отключаем сокет
        """
        await self.accept()
        self.chat_secret_key = (
            self.scope['url_route']['kwargs']['chat_secret_key']
        )
        self.chat = await self.get_chat()
        self.room_group_name = 'chat_%s' % self.chat_secret_key
        self.user = self.scope['user']

        await self.check_chat_access()

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
        """Перенаправление текста сообщения в функцию указанную в type"""
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'text_data': text_data,
            }
        )

    async def chat_message(self, event):
        """Отправка сообщения обратно через WebSocket"""
        message = await self.save_message(event['text_data'])
        text = self.format_message(message=message)
        await self.send(text_data=text)

    async def disconnect(self, code):
        """При отключение убирает анонима из чата"""
        if hasattr(self, "chat_subscribe"):
            await self.remove_user_from_room(self.chat_subscribe)
            await self.notify_users()
        if self.chat and self.user.is_anonymous:
            await self.set_connected_clients(disconnected=True)
        await super().disconnect(code)

    @database_sync_to_async
    def get_messages(self):
        """Получаем список сообщений связанные с чатом"""
        return list(
            Message.objects.filter(chat=self.chat).order_by('date_time')
        )

    async def send_old_message(self, messages):
        """Печатаем все старые сообщения при подключении"""
        for message in messages:
            await self.send(
                self.format_message(message=message)
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
        message = Message(
            chat=self.chat,
            text=message,
            is_psy_author=not self.user.is_anonymous
        )
        message.save()
        return message

    @database_sync_to_async
    def set_psy_in_chat(self):
        """Записываем психолга в чат"""
        if self.user.approved_by_moderator:
            self.chat.psychologist = self.user
            self.chat.save()

    @database_sync_to_async
    def set_connected_clients(self, disconnected=False):
        """
        Добавляет в модель клиента при подключении
        убирает при отключении
        """
        if not self.chat:
            return
        if disconnected:
            self.chat.connected_clients -= 1
        else:
            self.chat.connected_clients += 1
        self.chat.save()

    async def check_chat_access(self):
        """Проверка на доступ к чату и закрываем при отказе"""
        if not self.chat:
            await self.send_error_and_closed_chat(4004, 'Not found chat')
        elif not self.chat.active:
            await self.send_error_and_closed_chat(4005, 'Chat closed')
        elif (
            not self.user.is_anonymous
            and self.chat.psychologist_id
            and self.chat.psychologist_id != self.user.id
        ):
            await self.send_error_and_closed_chat(4006, 'Psychologist in caht')
        elif (
            not self.user.is_anonymous
            and not self.user.approved_by_moderator
        ):
            await self.send_error_and_closed_chat(
                4007, 'Documents not verifield'
            )
        elif self.user.is_anonymous and self.chat.connected_clients:
            await self.send_error_and_closed_chat(4008, 'Client in chat')

    async def send_error_and_closed_chat(self, code, error_message):
        """Отправка текста ошибки и закрытие чата"""
        await self.send(text_data=json.dumps({
            'error': error_message
        }))
        await super().disconnect(code)
        await self.close(code=code)

    def format_message(self, message):
        data = ({
            'message': message.text,
            'psy': message.is_psy_author,
            'date': message.date_time.isoformat()
        })
        return json.dumps(data, ensure_ascii=False)
