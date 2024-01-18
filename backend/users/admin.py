from django.contrib import admin

from .models import CustomUser, Education, CustomClientUser


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'scan',
                    'university', 'faculty',
                    'specialization', 'year_of_graduation', )


class EducationAdminInlineAdmin(admin.TabularInline):
    """Класс для вывода Сертификатов в User."""

    model = Education
    fields = ('scan',)


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    inlines = (EducationAdminInlineAdmin,)
    list_display = ('pk', 'email',
                    'first_name', 'last_name',
                    'approved_by_moderator', 'role', 'birth_date')
    list_filter = ('email', 'approved_by_moderator')
    search_fields = ('email',)


@admin.register(CustomClientUser)
class ClienAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email',
                    'first_name', 'last_name', 'birth_date')
