from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.permissions import (AllowAny, IsAuthenticated,)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from core.utils import get_confirmation_code
from users.models import CustomClientUser, Education
from .serializers import (UserSerializer, CustomClientUserSerializer,
                          EducationSerializer)

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
