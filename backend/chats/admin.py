from django.contrib import admin

from .models import Chat, Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Класс админки сообщений."""

    list_display = ('id',
                    'text', 'is_psy_author',
                    'date_time')


class MessageAdminInlineAdmin(admin.TabularInline):
    """Класс для вывода Сообщений в Чате."""

    model = Message
    readonly_fields = ('text',
                       'is_psy_author',
                       'date_time')


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    """Класс админки Чатов."""

    inlines = (MessageAdminInlineAdmin,)
    list_display = ('id',
                    'client', 'psychologist',
                    'active',
                    'chat_secret_key')
