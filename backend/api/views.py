from django.contrib.auth import get_user_model
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (UserSerializer, UserCreateSerializer, 
                          EducationSerializer, CustomClientUserSerializer)
from users.models import CustomClientUser


User = get_user_model()


# class UsersViewSet(mixins.UpdateModelMixin,
#                    mixins.DestroyModelMixin,
#                    mixins.CreateModelMixin,
#                    mixins.ListModelMixin,
#                    mixins.RetrieveModelMixin,
#                    viewsets.GenericViewSet):
#     """ViewSet для просмотра и редактирования данных пользователя."""

#     queryset = User.objects.filter(role='PSYCHOLOGIST')
#     serializer_class = UserSerializer
#     permission_classes = (AllowAny, )
#     http_method_names = ['get', 'post']
#     lookup_field = 'id'


class UsersViewSet(mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """ViewSet для просмотра пользователей и редактирования
    данных пользователя."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (AllowAny, )
    lookup_field = 'id'
    # search_fields = ('username', )

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
