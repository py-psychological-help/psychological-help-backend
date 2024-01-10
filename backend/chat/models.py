from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class Chat(models.Model):
    chat_secret_key = None
    consumer = models.ForeignKey(User, null=True,
                                 related_name="consumer_chats",
                                 on_delete=models.CASCADE)
    psychologist = models.ForeignKey(User, null=True,
                                     related_name="psychologist_chats",
                                     on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(str(self.consumer) + str(self.psychologist))


class Message(models.Model):
    
    chat = models.ForeignKey(Chat,
                                on_delete=models.CASCADE,
                                related_name='messages')
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
