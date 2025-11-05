"""
Модели для управления расписанием и слотами барберов.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import BarberProfile
from datetime import time, date, datetime, timedelta


class BarberScheduleSettings(models.Model):
    """
    Настройки расписания работы барбера (дефолтные).
    Каждый барбер имеет одну запись настроек.
    """

    WEEKDAY_CHOICES = [
        (0, _('Понедельник')),
        (1, _('Вторник')),
        (2, _('Среда')),
        (3, _('Четверг')),
        (4, _('Пятница')),
        (5, _('Суббота')),
        (6, _('Воскресенье')),
    ]

    barber = models.OneToOneField(
        BarberProfile,
        on_delete=models.CASCADE,
        related_name='schedule_settings',
        verbose_name=_('Барбер')
    )

    # Дни недели работы (хранятся как JSON список: [0,1,2,3,4] для пн-пт)
    working_weekdays = models.JSONField(
        _('Рабочие дни недели'),
        default=list,
        help_text=_('Список номеров дней недели (0=пн, 6=вс)')
    )

    # Время работы
    work_start_time = models.TimeField(
        _('Время начала работы'),
        default=time(9, 0)
    )
    work_end_time = models.TimeField(
        _('Время окончания работы'),
        default=time(18, 0)
    )

    # Перерыв
    break_start_time = models.TimeField(
        _('Время начала перерыва'),
        blank=True,
        null=True
    )
    break_end_time = models.TimeField(
        _('Время окончания перерыва'),
        blank=True,
        null=True
    )

    # Продолжительность одного сеанса (в минутах)
    slot_duration_minutes = models.PositiveIntegerField(
        _('Продолжительность сеанса (минуты)'),
        default=30,
        validators=[MinValueValidator(15), MaxValueValidator(240)]
    )

    # За сколько дней вперед открывается запись
    booking_advance_days = models.PositiveIntegerField(
        _('Дней для открытия записи вперед'),
        default=14,
        validators=[MinValueValidator(1), MaxValueValidator(90)],
        help_text=_('На сколько дней вперед клиенты могут записываться')
    )

    # Минимальное время до начала записи (в часах)
    min_booking_notice_hours = models.PositiveIntegerField(
        _('Минимальное время уведомления (часы)'),
        default=2,
        validators=[MinValueValidator(0), MaxValueValidator(72)],
        help_text=_('За сколько часов минимум нужно записываться')
    )

    is_active = models.BooleanField(
        _('Активно'),
        default=True,
        help_text=_('Автоматическая генерация слотов включена')
    )

    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)

    class Meta:
        verbose_name = _('Настройки расписания барбера')
        verbose_name_plural = _('Настройки расписаний барберов')
        ordering = ['barber']

    def __str__(self):
        return f'Настройки расписания: {self.barber}'

    def get_working_weekdays_display(self):
        """Получить названия рабочих дней недели."""
        weekday_names = dict(self.WEEKDAY_CHOICES)
        return [weekday_names[day] for day in sorted(self.working_weekdays)]

    def is_working_day(self, check_date):
        """Проверить, является ли день рабочим по умолчанию."""
        if isinstance(check_date, datetime):
            check_date = check_date.date()
        return check_date.weekday() in self.working_weekdays


class ScheduleOverride(models.Model):
    """
    Исключения и переопределения для конкретных дней.
    Позволяет барберу отметить день как нерабочий или изменить время работы.
    """

    OVERRIDE_TYPE_CHOICES = [
        ('day_off', _('Выходной день')),
        ('custom_hours', _('Изменение времени работы')),
        ('custom_break', _('Изменение перерыва')),
    ]

    barber = models.ForeignKey(
        BarberProfile,
        on_delete=models.CASCADE,
        related_name='schedule_overrides',
        verbose_name=_('Барбер')
    )

    date = models.DateField(_('Дата'))

    override_type = models.CharField(
        _('Тип исключения'),
        max_length=20,
        choices=OVERRIDE_TYPE_CHOICES,
        default='day_off'
    )

    # Для custom_hours
    custom_start_time = models.TimeField(
        _('Измененное время начала'),
        blank=True,
        null=True
    )
    custom_end_time = models.TimeField(
        _('Измененное время окончания'),
        blank=True,
        null=True
    )

    # Для custom_break
    custom_break_start = models.TimeField(
        _('Измененное время начала перерыва'),
        blank=True,
        null=True
    )
    custom_break_end = models.TimeField(
        _('Измененное время окончания перерыва'),
        blank=True,
        null=True
    )

    notes = models.TextField(
        _('Примечания'),
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)

    class Meta:
        verbose_name = _('Исключение в расписании')
        verbose_name_plural = _('Исключения в расписании')
        ordering = ['date']
        unique_together = ['barber', 'date']

    def __str__(self):
        return f'{self.barber} - {self.date} ({self.get_override_type_display()})'


class TimeSlot(models.Model):
    """
    Временной слот для записи.
    Генерируется автоматически на основе настроек расписания.
    """

    STATUS_CHOICES = [
        ('available', _('Доступен')),
        ('booked', _('Забронирован')),
        ('blocked', _('Заблокирован')),
    ]

    barber = models.ForeignKey(
        BarberProfile,
        on_delete=models.CASCADE,
        related_name='time_slots',
        verbose_name=_('Барбер')
    )

    date = models.DateField(_('Дата'))
    start_time = models.TimeField(_('Время начала'))
    end_time = models.TimeField(_('Время окончания'))

    status = models.CharField(
        _('Статус'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )

    # Для связи с бронированием
    booking = models.ForeignKey(
        'Booking',
        on_delete=models.SET_NULL,
        related_name='slots',
        verbose_name=_('Бронирование'),
        blank=True,
        null=True
    )

    # Автоматически сгенерирован или создан вручную
    is_auto_generated = models.BooleanField(
        _('Автоматически сгенерирован'),
        default=True
    )

    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)

    class Meta:
        verbose_name = _('Временной слот')
        verbose_name_plural = _('Временные слоты')
        ordering = ['date', 'start_time']
        unique_together = ['barber', 'date', 'start_time']
        indexes = [
            models.Index(fields=['barber', 'date', 'status']),
            models.Index(fields=['date', 'status']),
        ]

    def __str__(self):
        return f'{self.barber} - {self.date} {self.start_time}-{self.end_time} ({self.get_status_display()})'

    @property
    def is_available(self):
        """Проверить, доступен ли слот для бронирования."""
        return self.status == 'available' and self.date >= date.today()

    @property
    def datetime_start(self):
        """Получить datetime начала слота."""
        return datetime.combine(self.date, self.start_time)

    @property
    def datetime_end(self):
        """Получить datetime окончания слота."""
        return datetime.combine(self.date, self.end_time)


class Booking(models.Model):
    """
    Бронирование клиента.
    """

    STATUS_CHOICES = [
        ('pending', _('Ожидает подтверждения')),
        ('confirmed', _('Подтверждено')),
        ('cancelled', _('Отменено')),
        ('completed', _('Завершено')),
        ('no_show', _('Не явился')),
    ]

    barber = models.ForeignKey(
        BarberProfile,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name=_('Барбер')
    )

    # Информация о клиенте
    client_name = models.CharField(_('Имя клиента'), max_length=100)
    client_phone = models.CharField(_('Телефон клиента'), max_length=20)
    client_email = models.EmailField(_('Email клиента'), blank=True, null=True)

    # Дата и время бронирования
    booking_date = models.DateField(_('Дата бронирования'))
    booking_start_time = models.TimeField(_('Время начала'))
    booking_end_time = models.TimeField(_('Время окончания'))

    # Услуги и комментарии
    service_description = models.TextField(
        _('Описание услуги'),
        blank=True,
        null=True
    )
    client_notes = models.TextField(
        _('Заметки клиента'),
        blank=True,
        null=True
    )
    barber_notes = models.TextField(
        _('Заметки барбера'),
        blank=True,
        null=True
    )

    status = models.CharField(
        _('Статус'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # Стоимость
    price = models.DecimalField(
        _('Стоимость'),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)

    class Meta:
        verbose_name = _('Бронирование')
        verbose_name_plural = _('Бронирования')
        ordering = ['-booking_date', '-booking_start_time']
        indexes = [
            models.Index(fields=['barber', 'booking_date', 'status']),
            models.Index(fields=['booking_date', 'status']),
            models.Index(fields=['client_phone']),
        ]

    def __str__(self):
        return f'{self.client_name} - {self.barber} ({self.booking_date} {self.booking_start_time})'

    @property
    def datetime_start(self):
        """Получить datetime начала бронирования."""
        return datetime.combine(self.booking_date, self.booking_start_time)

    @property
    def datetime_end(self):
        """Получить datetime окончания бронирования."""
        return datetime.combine(self.booking_date, self.booking_end_time)

    @property
    def duration_minutes(self):
        """Получить продолжительность бронирования в минутах."""
        duration = self.datetime_end - self.datetime_start
        return int(duration.total_seconds() / 60)
