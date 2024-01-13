from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework import mixins, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (AllowAny, IsAuthenticated,)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.exceptions import PermissionDenied

from core.utils import get_confirmation_code, get_chat_id, create_secret_key
from core.emails import send_chat_url
from users.models import CustomClientUser, Education
from .serializers import (UserSerializer, CustomClientUserSerializer,
                          EducationSerializer, ChatSerializer,
                          MessageSerializer)
from chats.models import Chat, Message

User = get_user_model()


class UsersViewSet(mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """
    ViewSet для просмотра пользователей и редактирования
    данных пользователя.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (AllowAny, )
    lookup_field = 'id'

    def perform_create(self, serializer):
        serializer.save()
        user = User.objects.get(username=self.request.data.get('username'))
        confirmation_code = get_confirmation_code(user)
        serializer.save(
            confirmation_code=confirmation_code
        )


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
        request.user.delete()
        return Response("Ваш профиль удален.",
                        status=status.HTTP_204_NO_CONTENT)


class CustomClientUserViewSet(viewsets.ModelViewSet):
    queryset = CustomClientUser.objects.all()
    serializer_class = CustomClientUserSerializer
    http_method_names = ['post']
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        # тут будет создание чата
        return super().perform_create(serializer)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        email = request.data.get('email')
        client = get_object_or_404(CustomClientUser, email=email)
        chat = Chat.objects.create(client=client)
        create_secret_key(chat)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)


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
    """Вьюшка просмотра и удаления чата."""

    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    http_method_names = ['get', 'delete']
    pagination_class = None

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
    print(chat_id)
    chat = get_object_or_404(Chat, id=chat_id)
    if chat.psychologist == request.user:
        chat.active = False
        chat.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response("Вы не можете завершить чужой чат",
                    status=status.HTTP_403_FORBIDDEN)
