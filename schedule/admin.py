"""
Административная панель для управления расписаниями и бронированиями.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import BarberScheduleSettings, ScheduleOverride, TimeSlot, Booking


@admin.register(BarberScheduleSettings)
class BarberScheduleSettingsAdmin(admin.ModelAdmin):
    """Административная панель для настроек расписания барбера."""

    list_display = [
        'barber',
        'get_working_days',
        'work_start_time',
        'work_end_time',
        'slot_duration_minutes',
        'booking_advance_days',
        'is_active'
    ]
    list_filter = ['is_active', 'work_start_time', 'work_end_time']
    search_fields = ['barber__first_name', 'barber__last_name', 'barber__user__email']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (_('Барбер'), {
            'fields': ('barber',)
        }),
        (_('Рабочие дни и время'), {
            'fields': (
                'working_weekdays',
                'work_start_time',
                'work_end_time',
            )
        }),
        (_('Перерыв'), {
            'fields': ('break_start_time', 'break_end_time'),
            'classes': ('collapse',)
        }),
        (_('Настройки слотов'), {
            'fields': (
                'slot_duration_minutes',
                'booking_advance_days',
                'min_booking_notice_hours',
            )
        }),
        (_('Статус'), {
            'fields': ('is_active',)
        }),
        (_('Служебная информация'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_working_days(self, obj):
        """Отображение рабочих дней."""
        days = obj.get_working_weekdays_display()
        return ', '.join(str(day) for day in days) if days else _('Не указаны')
    get_working_days.short_description = _('Рабочие дни')


@admin.register(ScheduleOverride)
class ScheduleOverrideAdmin(admin.ModelAdmin):
    """Административная панель для исключений в расписании."""

    list_display = [
        'barber',
        'date',
        'override_type',
        'custom_start_time',
        'custom_end_time',
    ]
    list_filter = ['override_type', 'date']
    search_fields = ['barber__first_name', 'barber__last_name', 'notes']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (_('Основная информация'), {
            'fields': ('barber', 'date', 'override_type')
        }),
        (_('Измененное время работы'), {
            'fields': ('custom_start_time', 'custom_end_time'),
            'classes': ('collapse',)
        }),
        (_('Измененный перерыв'), {
            'fields': ('custom_break_start', 'custom_break_end'),
            'classes': ('collapse',)
        }),
        (_('Примечания'), {
            'fields': ('notes',)
        }),
        (_('Служебная информация'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    """Административная панель для временных слотов."""

    list_display = [
        'barber',
        'date',
        'start_time',
        'end_time',
        'status',
        'booking',
        'is_auto_generated'
    ]
    list_filter = ['status', 'date', 'is_auto_generated']
    search_fields = ['barber__first_name', 'barber__last_name']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (_('Основная информация'), {
            'fields': ('barber', 'date', 'start_time', 'end_time')
        }),
        (_('Статус и бронирование'), {
            'fields': ('status', 'booking', 'is_auto_generated')
        }),
        (_('Служебная информация'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_blocked', 'mark_as_available']

    def mark_as_blocked(self, request, queryset):
        """Заблокировать выбранные слоты."""
        updated = queryset.filter(status='available').update(status='blocked')
        self.message_user(request, _(f'{updated} слотов заблокировано.'))
    mark_as_blocked.short_description = _('Заблокировать выбранные слоты')

    def mark_as_available(self, request, queryset):
        """Сделать выбранные слоты доступными."""
        updated = queryset.filter(status='blocked', booking__isnull=True).update(status='available')
        self.message_user(request, _(f'{updated} слотов разблокировано.'))
    mark_as_available.short_description = _('Разблокировать выбранные слоты')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Административная панель для бронирований."""

    list_display = [
        'id',
        'client_name',
        'client_phone',
        'barber',
        'booking_date',
        'booking_start_time',
        'status',
        'price'
    ]
    list_filter = ['status', 'booking_date', 'barber']
    search_fields = [
        'client_name',
        'client_phone',
        'client_email',
        'barber__first_name',
        'barber__last_name'
    ]
    date_hierarchy = 'booking_date'
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (_('Информация о клиенте'), {
            'fields': ('client_name', 'client_phone', 'client_email')
        }),
        (_('Детали бронирования'), {
            'fields': (
                'barber',
                'booking_date',
                'booking_start_time',
                'booking_end_time',
                'service_description',
                'price'
            )
        }),
        (_('Статус'), {
            'fields': ('status',)
        }),
        (_('Заметки'), {
            'fields': ('client_notes', 'barber_notes'),
            'classes': ('collapse',)
        }),
        (_('Служебная информация'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_confirmed', 'mark_as_cancelled', 'mark_as_completed']

    def mark_as_confirmed(self, request, queryset):
        """Подтвердить выбранные бронирования."""
        updated = queryset.filter(status='pending').update(status='confirmed')
        self.message_user(request, _(f'{updated} бронирований подтверждено.'))
    mark_as_confirmed.short_description = _('Подтвердить выбранные бронирования')

    def mark_as_cancelled(self, request, queryset):
        """Отменить выбранные бронирования."""
        updated = queryset.exclude(status__in=['completed', 'cancelled']).update(status='cancelled')
        # Освободить слоты
        from .models import TimeSlot
        for booking in queryset.filter(status='cancelled'):
            TimeSlot.objects.filter(booking=booking).update(status='available', booking=None)
        self.message_user(request, _(f'{updated} бронирований отменено.'))
    mark_as_cancelled.short_description = _('Отменить выбранные бронирования')

    def mark_as_completed(self, request, queryset):
        """Завершить выбранные бронирования."""
        updated = queryset.filter(status='confirmed').update(status='completed')
        self.message_user(request, _(f'{updated} бронирований завершено.'))
    mark_as_completed.short_description = _('Завершить выбранные бронирования')
