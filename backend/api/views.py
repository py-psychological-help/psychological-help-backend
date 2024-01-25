from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (AllowAny, IsAuthenticated,)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from chats.models import Chat
from core.emails import send_chat_url
from core.utils import get_chat_id
from users.models import CustomClientUser, Education
from .serializers import (UserSerializer, ClientSerializer,
                          EducationSerializer, ChatSerializer,
                          MessageSerializer)
from .filters import ChatFilter
from .permissions import ApprovedByModerator


User = get_user_model()


class UserMe(APIView):
    """Вьюсет для своей страницы."""

    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.get(request)

    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.get(request)

    def delete(self, request, *args, **kwargs):
        # request.user.delete()
        response_message = {'message': "Ваш профиль удален."}
        return Response(response_message,
                        status=status.HTTP_204_NO_CONTENT)


class CustomClientUserViewSet(viewsets.ModelViewSet):
    """Вьюсет создания Клиента. Автоматические создается чат."""

    queryset = CustomClientUser.objects.all()
    serializer_class = ClientSerializer
    http_method_names = ['post']
    permission_classes = (AllowAny,)


class EducationViewSet(viewsets.ModelViewSet):
    """Эндпоинт для просмотра списка, добавления и удаления сертификатов."""

    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    http_method_names = ['get', 'post', 'delete']
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def list(self, request, *args, **kwargs):
        psychologist = request.user
        queryset = self.queryset.filter(user=psychologist)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ChatViewSet(viewsets.ModelViewSet):
    """Вьюшка просмотра чата, списка и удаления."""

    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    http_method_names = ['get', 'delete']
    pagination_class = None
    permission_classes = (ApprovedByModerator,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ChatFilter

    def retrieve(self, request, *args, **kwargs):
        chat_secret_key = self.kwargs.get('pk')
        chat_id = get_chat_id(chat_secret_key)
        chat = get_object_or_404(Chat, id=chat_id)
        serializer = self.get_serializer(chat)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        chat_secret_key = self.kwargs.get('pk')
        chat_id = get_chat_id(chat_secret_key)
        chat = get_object_or_404(Chat, id=chat_id)
        self.perform_destroy(chat)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageViewSet(viewsets.ModelViewSet):
    """Создание сообщения и просмотр списка сообщений."""

    serializer_class = MessageSerializer
    permission_classes = (AllowAny,)
    pagination_class = None

    def get_queryset(self):
        chat_secret_key = self.kwargs.get('chat_secret_key')
        chat_id = get_chat_id(chat_secret_key)
        chat = get_object_or_404(Chat, pk=chat_id)
        return chat.messages.all()

    def perform_create(self, serializer):
        chat_secret_key = self.kwargs.get('chat_secret_key')
        chat_id = get_chat_id(chat_secret_key)
        author = self.request.user
        chat = get_object_or_404(Chat, pk=chat_id)
        if author.is_anonymous:
            serializer.save(is_psy_author=False, chat=chat)
            return
        if author != chat.psychologist:
            raise PermissionDenied("Нельзя писать за другого психолога!")
        serializer.save(is_psy_author=True, chat=chat)


@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def activate_chat(request, chat_secret_key):
    """Привязывает психолога к чату и отправляет клиенту email."""
    chat_id = get_chat_id(chat_secret_key)
    chat = get_object_or_404(Chat, id=chat_id)
    send_chat_url(chat)
    if chat.psychologist is None:
        chat.psychologist = request.user
        chat.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response("У этого чата уже есть Психолог. Письмо направлено",
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def finish_chat(request, chat_secret_key):
    """Меняет статус чата на Завершенный."""
    chat_id = get_chat_id(chat_secret_key)
    chat = get_object_or_404(Chat, id=chat_id)
    if chat.psychologist == request.user:
        chat.active = False
        chat.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response("Вы не можете завершить чужой чат",
                    status=status.HTTP_403_FORBIDDEN)
