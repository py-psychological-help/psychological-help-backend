from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class Chat(models.Model):
    """Класс модели Чат. Диалог между пользователем и психологом."""
    id = models.CharField(_("id"),
                          primary_key=True)
    chat_secret_key = None
    consumer_id = models.ForeignKey(User, null=True, related_name="chats")
    psychologist_id = models.ForeignKey(User, null=True, related_name="chats")
    is_active = models.BooleanField(default=True)
    message_set = Message.objects.get(chat_id=id)
    psy_messages = Message.objects.get(author=psychologist_id)
    consumer_messages = Message.objects.get(author=consumer_id)

    class Meta:
        verbose_name = "чат"
        verbose_name_plural = "чаты"


class Message(models.Model):
    id = models.CharField(_("id"),
                          primary_key=True)
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="messages")
    date_time = models.DateTimeField("Дата отправки",
                                     auto_now_add=True,
                                     db_index=True)
    text = models.TextField("Текст сообщения")

    class Meta:
        ordering = ('-date_time',)
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"