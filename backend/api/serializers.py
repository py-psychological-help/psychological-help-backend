from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.contrib.auth import get_user_model

from chat.models import Chat, Message


User = get_user_model()


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Chat


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('text', 'author')
        read_only_fields = ('author', )
        model = Message
