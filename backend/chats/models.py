from django.db import models
from django.contrib.auth import get_user_model
from users.models import CustomClientUser


User = get_user_model()


class Chat(models.Model):
    """Модель чатов."""

    client = models.OneToOneField(CustomClientUser,
                                  null=False,
                                  blank=False,
                                  related_name="client_chats",
                                  on_delete=models.CASCADE)
    psychologist = models.ForeignKey(User,
                                     null=True,
                                     blank=True,
                                     related_name="psychologist_chats",
                                     on_delete=models.SET_NULL)
    date_time = models.DateTimeField("Дата создания",
                                     auto_now_add=True,
                                     db_index=True)
    active = models.BooleanField(default=True)
    chat_secret_key = models.CharField(max_length=50, blank=True)
    connected_clients = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.client)


class Message(models.Model):
    """Модель сообщейний."""

    text = models.TextField("Текст сообщения")
    date_time = models.DateTimeField("Дата отправки",
                                     auto_now_add=True,
                                     db_index=True)
    chat = models.ForeignKey(Chat,
                             on_delete=models.CASCADE,
                             related_name="messages")
    is_psy_author = models.BooleanField(blank=False)
