import json
import random

from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from channels.db import database_sync_to_async
from nickname_generator import generate

from .models import Chat, Message, Nikname


GENERAL_CHAT = 'general'


class ChatConsumer(GenericAsyncAPIConsumer):
    """Чат one to one психолог - аноним"""

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
        """
        Сохраняем сообщение и пернаправляем данные для отправки
        в функцию указанную в "type"
        Если прилетает JSON {"action": "archive_chat"}
        закрывем соединение и переводим статус чата в неактивное
        """
        text = json.dumps(
            {'message': 'Chat in closed'}, ensure_ascii=False
        )
        try:
            data = json.loads(text_data)
            action = data.get('action')
            if action == 'archive_chat':
                await self.archive_chat()
        except Exception:
            message = await self.save_message(text_data)
            text = self.format_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'text': text
            }
        )

    async def chat_message(self, event):
        """Отправка сообщения обратно через WebSocket"""
        await self.send(text_data=event['text'])

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
        if not self.chat.psychologist and self.user.approved_by_moderator:
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

    async def archive_chat(self):
        """Переводим чат в неактивные и закрываем соединения"""
        await self.chat_not_active()
        await super().disconnect(1000)
        await self.close()

    @database_sync_to_async
    def chat_not_active(self):
        self.chat.active = False
        self.chat.save()


class GeneralChatConsumer(GenericAsyncAPIConsumer):
    """Чат many to many общий чат психологов и анонимов"""

    async def connect(self):
        """
        Подключаемся к чату
        если аноним - генерируем никнейм
        если психолог - используем его имя и фамилию
        """
        self.room_name = GENERAL_CHAT
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope['user']

        if self.user.is_anonymous:
            self.username = await self.get_nikname()
        else:
            self.username = f'{self.user.last_name} {self.user.first_name}'

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        if self.user.is_anonymous:
            await self.remove_nickname()
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": text_data,
                "nikname": self.username,
            }
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "nickname": event["nikname"]
                },
                ensure_ascii=False
            )
        )

    @database_sync_to_async
    def get_nikname(self):
        """Генирация уникального никнейма"""
        nikname = generate()
        if Nikname.objects.filter(nikname=nikname).exists():
            self.get_nikname()
        nikname_obj = Nikname(nikname=nikname)
        nikname_obj.save()
        return nikname

    @database_sync_to_async
    def remove_nickname(self):
        """Удаление никнейма"""
        Nikname.objects.filter(nikname=self.username).delete()
