from django.db import models
from messages.models import Message
from users.models import User
# Create your models here.


class Chat(models.Model):
    """Класс модели Чат. Диалог между пользователем и психологом."""
    id = models.CharField(_("id"),
                          primary_key=True,
                          editable=False,
                          max_length=50)
    chat_secret_key = None
    consumer_id = models.ForeignKey(User, null=True, related_name="chats")
    psychologist_id = models.ForeignKey(User, null=True, related_name="chats")
    is_active = models.BooleanField(default=True)
    psy_messages = Message.objects.get(author=psychologist_id)
    consumer_messages = Message.objects.get(author=consumer_id)

    class Meta:
        verbose_name = "чат"
        verbose_name_plural = "чаты"


class Message(models.Model):
    id = models.CharField(_("id"),
                          primary_key=True,
                          editable=False,
                          max_length=50)
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="messages")
    date_time = models.DateTimeField("Дата отправки",
                                     auto_now_add=True,
                                     db_index=True)
    text = models.TextField("Текст сообщения")

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"
