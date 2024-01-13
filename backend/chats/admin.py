from django.contrib import admin

from .models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'client', 'psychologist',
                    'active')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'text', 'is_psy_author',
                    'date_time')
