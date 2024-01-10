from django.contrib import admin

from .models import Chat


@admin.register(Chat)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat_secret_key',
                    'consumer', 'psychologist',
                    'is_active')
