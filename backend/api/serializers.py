from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.contrib.auth import get_user_model

from chat.models import Chat, Message


User = get_user_model()


class ChatSerializer(serializers.ModelSerializer):
    consumer = SlugRelatedField(slug_field='username',
                                read_only=True)
    psychologist = SlugRelatedField(slug_field='username',
                                    read_only=True)

    class Meta:
        fields = '__all__'
        model = Chat


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ['chat']
        model = Message
