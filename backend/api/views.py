from django.contrib.auth import get_user_model

from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404

from .permissions import AuthorOrReadOnly
from chat.models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from .viewsets import ListCreateViewSet
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

User = get_user_model()

class ChatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    pagination_class = LimitOffsetPagination
    #permission_classes = (AuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    # permission_classes = (AuthorOrReadOnly,)
    permission_classes = (AllowAny,)

    def get_queryset(self):
        chat_id = self.kwargs.get('chat_id')
        chat = get_object_or_404(Chat, pk=chat_id)
        return chat.messages.all()

    def perform_create(self, serializer):
        chat_id = self.kwargs.get('chat_id')
        # author = self.request.user
        author = get_object_or_404(User, id=1) # костыль т.к. нет аутентификации 
        chat = get_object_or_404(Chat, pk=chat_id)
        serializer.save(author=author, chat=chat)
