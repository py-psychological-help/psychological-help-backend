from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email',
                    'first_name', 'last_name',
                    'approved_by_moderator', 'role')
    list_filter = ('email', 'approved_by_moderator')
    search_fields = ('email',)

