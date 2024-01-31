import json

from channels.db import database_sync_to_async
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer

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

        error_message = await self.check_chat_access()

        if error_message:
            await self.send_error_message(error_message)
            await self.close()
            await super().disconnect(4009)

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
        if self.user.is_anonymous:
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
        self.chat.psychologist = self.user
        self.chat.save()

    @database_sync_to_async
    def set_connected_clients(self, disconnected=False):
        """
        Добавляет в модель клиента при подключении
        убирает при отключении
        """
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
        if (
            not self.user.is_anonymous
            and self.chat.psychologist_id
            and self.chat.psychologist_id != self.user.id
        ):
            return '3 Психолог уже есть'
        if not self.user.is_anonymous and not self.user.approved_by_moderator:
            return '4 Дождитесь проверки документов'
        if self.user.is_anonymous and self.chat.connected_clients:
            return '5 В чате уже есть клиент'

    async def send_error_message(self, error_message):
        """Отправка текста ошибки"""
        await self.send(self.format_message(error_message=error_message))

    def format_message(self, message=None, error_message=None):
        data = {'error_msg': error_message}
        if message:
            data.update({
                'message': message.text,
                'psy': message.is_psy_author,
                'date': message.date_time.isoformat()
            })
        return json.dumps(data)
