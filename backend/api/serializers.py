import base64

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from rest_framework import serializers

from users.models import Education, CustomClientUser

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    """Сериализатор картинок в HEX."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class EducationSerializer(serializers.ModelSerializer):
    scan = Base64ImageField(required=True, allow_null=False)

    class Meta:
        model = Education
        fields = ('id',
                  'university',
                  'faculty',
                  'specialization',
                  'year_of_graduation',
                  'scan'
                  )
        read_only_fields = ('id',)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор отображения Пользователей."""

    photo = Base64ImageField(required=False, allow_null=True)
    education = EducationSerializer(many=True, read_only=True)
    approved = serializers.BooleanField(source='approved_by_moderator',
                                        read_only=True)

    class Meta:
        fields = ('id',
                  'first_name',
                  'last_name',
                  'birth_date',
                  'email',
                  'photo',
                  'education',
                  'approved'
                  )
        read_only_fields = ('approved',)
        model = User


class UserCreateSerializer(UserSerializer):
    """Сериализатор создания пользователей."""

    email = serializers.EmailField(required=True,
                                   max_length=settings.MAX_EMAIL_LEN)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    approved = serializers.BooleanField(source='approved_by_moderator',
                                        read_only=True)

    class Meta:
        model = User
        fields = ('id',
                  'email',
                  'first_name',
                  'last_name',
                  'password',
                  'approved')
        read_only_fields = ('id',
                            'first_name',
                            'last_name',
                            'approved')
        extra_kwargs = {'password': {'write_only': True}, }

    def validate_email(self, email):
        """Валидация почты."""
        if User.objects.filter(email=email):
            raise serializers.ValidationError('Пользователь с таким email уже '
                                              'существует')
        return email

    def validate_first_name(self, first_name):
        if len(first_name) > settings.MAX_USER_LEN:
            raise serializers.ValidationError('Имя не может быть длиннее '
                                              f'{settings.MAX_USER_LEN} '
                                              'символов')
        return first_name

    def validate_last_name(self, last_name):
        if len(last_name) > settings.MAX_USER_LEN:
            raise serializers.ValidationError('Имя не может быть длиннее 150 '
                                              'символов')
        return last_name

    def create(self, validated_data):
        """Переопределение create для хэширования паролей."""
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)


class CustomClientUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomClientUser
        fields = ('id',
                  'email',
                  'first_name',
                  'last_name',)
        read_only_fields = ('id',)