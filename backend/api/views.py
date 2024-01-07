from django.shortcuts import render
from rest_framework import viewsets
# Create your views here.

from chat.models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer


class ChatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        chat_id = self.kwargs.get('chat_id')
        new_queryset = Message.objects.filter(chat=chat_id)
        return new_queryset
