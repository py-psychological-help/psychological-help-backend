from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (AllowAny, IsAuthenticated,)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.exceptions import PermissionDenied

from core.utils import get_confirmation_code
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
    http_method_names = ['get', 'post', 'put', 'patch']

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


class CustomClientUserViewSet(viewsets.ModelViewSet):
    queryset = CustomClientUser.objects.all()
    serializer_class = CustomClientUserSerializer
    http_method_names = ['post']

    def perform_create(self, serializer):
        # тут будет создание чата
        return super().perform_create(serializer)


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
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    #permission_classes = (AuthorOrReadOnly,)
    http_method_names = ['get', 'delete']
    pagination_class = None

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
        author = self.request.user
        chat = get_object_or_404(Chat, pk=chat_id)
        if author.is_anonymous:
            serializer.save(is_psy_author=False, chat=chat)
            return
        if author != chat.psychologist:
            raise PermissionDenied("Нельзя писать за другого психолога!")
        serializer.save(is_psy_author=True, chat=chat)

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)
    

@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def activate_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    send_chat_url(chat)
    if chat.psychologist is None:
        chat.psychologist = request.user
        chat.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response("У этого чата уже есть Психолог",
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def finish_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if chat.psychologist == request.user:
        chat.is_finished = True
        chat.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response("Вы не можете завершить чужой чат",
                    status=status.HTTP_403_FORBIDDEN)
