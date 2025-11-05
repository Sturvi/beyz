"""
Административная панель для управления пользователями и профилями.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, BarberProfile


class BarberProfileInline(admin.StackedInline):
    """Inline для профиля барбера."""
    model = BarberProfile
    can_delete = False
    verbose_name_plural = 'Профиль барбера'
    fields = (
        'first_name', 'last_name', 'phone', 'bio',
        'experience_years', 'specializations', 'is_available', 'photo'
    )


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Административная панель для модели User."""

    inlines = [BarberProfileInline]

    list_display = ('email', 'role', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('email',)
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Права доступа'), {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser')
        }),
        (_('Важные даты'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'is_staff', 'is_active'),
        }),
    )

    readonly_fields = ('date_joined', 'last_login')


@admin.register(BarberProfile)
class BarberProfileAdmin(admin.ModelAdmin):
    """Административная панель для профилей барберов."""

    list_display = (
        'full_name', 'user', 'phone', 'experience_years',
        'is_available', 'created_at'
    )
    list_filter = ('is_available', 'experience_years', 'created_at')
    search_fields = ('first_name', 'last_name', 'user__email', 'phone')
    ordering = ('last_name', 'first_name')

    fieldsets = (
        (_('Основная информация'), {
            'fields': ('user', 'first_name', 'last_name', 'phone', 'photo')
        }),
        (_('Профессиональная информация'), {
            'fields': ('experience_years', 'specializations', 'bio', 'is_available')
        }),
        (_('Даты'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')
