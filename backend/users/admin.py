from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

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
class CustomUserAdmin(UserAdmin):
    inlines = (EducationAdminInlineAdmin,)
    list_display = ('pk', 'email',
                    'first_name', 'last_name',
                    'approved_by_moderator', 'role', 'birth_date')
    list_filter = ('email', 'approved_by_moderator')
    search_fields = ('email',)
    ordering = ("email",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            ("Персональные данные"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "patronymic",
                    "photo",
                )
            },
        ),
        (
            ("Права"),
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "approved_by_moderator",
                    "is_reg_confirm_sent",
                    "is_approve_sent",
                    "confirmation_code",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            ("Даты"),
            {
                "fields": (
                    "birth_date",
                    "last_login",
                    "date_joined",
                )
            },
        ),
        ((None), {"fields": ("greeting",)}),
    )
    add_fieldsets = (
        (
            None,
            {"fields": ("email", "password1", "password2")},
        ),
        (
            ("Персональные данные"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "patronymic",
                    "photo",
                )
            },
        ),
        (
            ("Права"),
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "approved_by_moderator",
                    "is_reg_confirm_sent",
                    "is_approve_sent",
                    "confirmation_code",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            ("Даты"),
            {
                "fields": (
                    "birth_date",
                    "last_login",
                    "date_joined",
                )
            },
        ),
        ((None), {"fields": ("greeting",)}),
    )


@admin.register(CustomClientUser)
class ClienAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email',
                    'first_name', 'last_name', 'birth_date')
