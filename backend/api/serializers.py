import base64

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import Document, CustomClientUser
from chats.models import Chat, Message
from users.validators import (AlphanumericValidator,
                              EmailSymbolsValidator,
                              NameSpacesValidator,
                              NameSymbolsValidator,
                              PasswordContentValidator,
                              PasswordGroupsValidator,
                              birthday_validator)

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    """Сериализатор картинок в Base64."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class DocumentSerializer(serializers.ModelSerializer):
    """Сериализатор объектов Документы."""

    scan = Base64ImageField(required=True, allow_null=False)

    class Meta:
        model = Document
        fields = ('id',
                  'name',
                  'scan'
                  )
        read_only_fields = ('id',)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор отображения Пользователей."""

    photo = Base64ImageField(required=False, allow_null=True)
    documents = DocumentSerializer(source='document', many=True,
                                   read_only=True)
    approved = serializers.BooleanField(source='approved_by_moderator',
                                        read_only=True)

    class Meta:
        fields = ('id',
                  'first_name',
                  'last_name',
                  'birth_date',
                  'email',
                  'photo',
                  'approved',
                  'documents',
                  )
        read_only_fields = ('approved', 'email', 'id')
        model = User


class UserChatSerializer(serializers.ModelSerializer):
    """Вложенный в чат сериализатор пользователей."""

    photo = Base64ImageField(required=False, allow_null=True)
    birth_date = serializers.DateField(
        read_only=True
    )

    class Meta:
        fields = ('first_name',
                  'last_name',
                  'birth_date',
                  'photo',
                  'greeting')
        read_only_fields = ('first_name',
                            'last_name',
                            'birth_date',
                            'photo',)
        model = User


class UserCreateSerializer(UserSerializer):
    """Сериализатор создания пользователей."""

    email = serializers.EmailField(
        required=True,
        max_length=settings.MAX_EMAIL_LEN,
        validators=[AlphanumericValidator,
                    EmailSymbolsValidator,
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message='Пользователь с таким email уже существует')])
    first_name = serializers.CharField(required=True,
                                       max_length=settings.MAX_USER_LEN,
                                       validators=[NameSpacesValidator,
                                                   NameSymbolsValidator, ])
    last_name = serializers.CharField(required=True,
                                      max_length=settings.MAX_USER_LEN,
                                      validators=[NameSpacesValidator,
                                                  NameSymbolsValidator, ])
    approved = serializers.BooleanField(source='approved_by_moderator',
                                        read_only=True)
    password = serializers.CharField(required=True,
                                     min_length=8,
                                     max_length=20,
                                     write_only=True,
                                     validators=[PasswordContentValidator,
                                                 PasswordGroupsValidator, ])
    birth_date = serializers.DateField(required=True,
                                       validators=[birthday_validator, ])

    class Meta:
        model = User
        fields = ('id',
                  'email',
                  'first_name',
                  'last_name',
                  'birth_date',
                  'password',
                  'approved',
                  )
        read_only_fields = ('id',
                            'first_name',
                            'last_name',
                            'approved')

    def create(self, validated_data):
        """Переопределение create для хэширования паролей."""
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)


class ClientSerializer(serializers.ModelSerializer):
    """Сериализатор клиентов."""

    class Meta:
        model = CustomClientUser
        fields = ('id',
                  'email',
                  'first_name',
                  'complaint',
                  )
        read_only_fields = ('id',)


class MessageSerializer(serializers.ModelSerializer):
    """Сериализатор сообщений."""

    is_author_me = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'text',
            'date_time',
            'is_author_me',
            'author')
        read_only_fields = (
            'id',
            'date_time',
            'is_author_me',
            'author')
        model = Message

    def get_is_author_me(self, message):
        request_user = self.context.get('request').user
        if request_user.is_anonymous:
            return not message.is_psy_author
        author = None
        if message.is_psy_author:
            author = message.chat.psychologist
        return author == request_user

    def get_author(self, message):
        if message.is_psy_author:
            if not message.chat.psychologist:
                return None
            return message.chat.psychologist.id
        return message.chat.client.id


class ChatSerializer(serializers.ModelSerializer):
    """Сериализатор чатов."""

    client = ClientSerializer(many=False)
    psychologist = UserChatSerializer(many=False)
    messages = MessageSerializer(many=True)
    new = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'chat_secret_key',
            'active',
            'new',
            'client',
            'psychologist',
            'messages',)
        model = Chat

    def get_new(self, chat):
        return chat.psychologist is None
