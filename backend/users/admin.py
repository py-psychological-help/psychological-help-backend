from django.contrib import admin

from .models import CustomUser, Education, CustomClientUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email',
                    'first_name', 'last_name',
                    'approved_by_moderator', 'role', 'birth_date')
    list_filter = ('email', 'approved_by_moderator')
    search_fields = ('email',)


@admin.register(Education)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user',
                    'university', 'faculty',
                    'specialization', 'year_of_graduation')


@admin.register(CustomClientUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email',
                    'first_name', 'last_name', 'birth_date')
