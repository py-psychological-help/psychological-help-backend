from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email',
                    'first_name', 'second_name',
                    'approved_by_moderator', 'education')
    list_editable = ('username', 'email',
                     'first_name', 'second_name',
                     'approved_by_moderator')
    list_filter = ('username', 'email', 'approved_by_moderator')
    search_fields = ('username', 'email')
