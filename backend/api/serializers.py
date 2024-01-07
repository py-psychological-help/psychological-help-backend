from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.contrib.auth import get_user_model

from chat.models import Chat, Message


User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    chat = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message


class ChatSerializer(serializers.ModelSerializer):
    consumer = SlugRelatedField(slug_field='username',
                                read_only=True)
    psychologist = SlugRelatedField(slug_field='username',
                                    read_only=True)
    messages = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['consumer', 'psychologist', 'messages']
