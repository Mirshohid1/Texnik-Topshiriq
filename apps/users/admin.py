from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    # Переопределяем поля, которые будут отображаться в списке пользователей
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active', 'date_joined', 'last_login')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'role')
    ordering = ('-date_joined',)
    readonly_fields = ('last_login', 'date_joined')

    # Добавление полей для создания и редактирования пользователей
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_staff', 'is_active'),
        }),
    )

    # Определение действий (если нужно)
    actions = ['make_admin', 'make_user']

    def make_admin(self, request, queryset):
        queryset.update(role='admin')
    make_admin.short_description = "Назначить выбранных пользователей администраторами"

    def make_user(self, request, queryset):
        queryset.update(role='user')
    make_user.short_description = "Назначить выбранных пользователей обычными пользователями"


# Регистрируем модель и кастомную админку
admin.site.register(User, CustomUserAdmin)
