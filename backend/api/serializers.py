from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.contrib.auth import get_user_model

from chat.models import Chat, Message


User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Message
        exclude = ('chat_id',)


class ChatListSerializer(serializers.ModelSerializer):
    consumer_id = SlugRelatedField(slug_field='username',
                                   read_only=True)
    psychologist_id = SlugRelatedField(slug_field='username',
                                       read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['consumer_id', 'psychologist_id', 'last_message']

    def get_last_message(self, instance):
        message = instance.message_set.first()
        return MessageSerializer(instance=message)


class ChatSerializer(serializers.ModelSerializer):
    consumer_id = SlugRelatedField(slug_field='username',
                                   read_only=True)
    psychologist_id = SlugRelatedField(slug_field='username',
                                       read_only=True)
    message_set = MessageSerializer(many=True)
    psy_messages = MessageSerializer(many=True)
    consumer_messages = MessageSerializer(many=True)

    class Meta:
        model = Chat
        fields = ['consumer_id', 'psychologist_id', 'message_set']
