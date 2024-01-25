import json

from asgiref.sync import sync_to_async
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
    serializer_class = ChatSerializer
    lookup_field = "pk"

    @action()
    async def send(self, message):
        raise

    async def disconnect(self, code):
        if hasattr(self, "chat_subscribe"):
            await self.remove_user_from_room(self.chat_subscribe)
            await self.notify_users()
        await super().disconnect(code)

    @action()
    async def join_chat(self, pk, **kwargs):
        self.chat_subscribe = pk
        await self.add_user_to_room(pk)
        await self.notify_users()

    @action()
    async def leave_chat(self, pk, **kwargs):
        await self.remove_user_from_chat(pk)

    @action()
    async def create_message(self, message, **kwargs):
        # chat: Chat = await self.get_chat(pk=1)
        # await database_sync_to_async(Message.objects.create)(
        #     chat=chat,
        #     # user=self.scope["user"],
        #     text=message
        # )
        print(message)

    @action()
    async def subscribe_to_messages_in_chat(self, pk, **kwargs):
        await self.message_activity.subscribe(chat=pk)

    @model_observer(Message)
    async def message_activity(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @message_activity.groups_for_signal
    def message_activity(self, instance: Message, **kwargs):
        yield f'chat__{instance.chat_id}'
        yield f'pk__{instance.pk}'

    @message_activity.groups_for_consumer
    def message_activity(self, chat=None, **kwargs):
        if chat is not None:
            yield f'chat__{chat}'

    @message_activity.serializer
    def message_activity(self, instance: Message, action, **kwargs):
        return dict(data=MessageSerializer(instance).data, action=action.value, pk=instance.pk)

    async def notify_users(self):
        chat: Chat = await self.get_chat(self.chat_subscribe)
        for group in self.groups:
            await self.channel_layer.group_send(
                group,
                {
                    'type': 'update_users',
                    'usuarios': await self.current_users(chat)
                }
            )

    async def update_users(self, event: dict):
        await self.send(text_data=json.dumps({'usuarios': event["usuarios"]}))

    @database_sync_to_async
    def get_chat(self, pk: int) -> Chat:
        return Chat.objects.get(pk=pk)

    @database_sync_to_async
    def current_users(self, chat: Chat):
        return [UserSerializer(user).data for user in chat.current_users.all()]

    @database_sync_to_async
    def remove_user_from_caht(self, chat):
        user: User = self.scope["user"]
        user.current_chat.remove(chat)

    @database_sync_to_async
    def add_user_to_chat(self, pk):
        user: User = self.scope["user"]
        if not user.current_chat.filter(pk=self.chat_subscribe).exists():
            user.current_chat.add(Chat.objects.get(pk=pk))


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