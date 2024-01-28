from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Document, CustomClientUser


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'scan', )


class DocumentAdminInlineAdmin(admin.TabularInline):
    """Класс для вывода Сертификатов в User."""

    model = Document
    fields = ('scan',)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = (DocumentAdminInlineAdmin,)
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
