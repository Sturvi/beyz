"""
Views для управления расписанием, слотами и бронированиями.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.db.models import Q
from datetime import date, datetime, timedelta
import calendar

from .models import (
    BarberScheduleSettings,
    ScheduleOverride,
    TimeSlot,
    Booking
)
from .forms import (
    BarberScheduleSettingsForm,
    ScheduleOverrideForm,
    BookingForm
)
from .services.slot_generator import SlotGeneratorService


@login_required
def schedule_settings_view(request):
    """
    Страница настроек расписания барбера.
    """
    if not request.user.is_barber:
        messages.error(request, _('Только барберы могут управлять расписанием.'))
        return redirect('accounts:dashboard')

    try:
        barber_profile = request.user.barber_profile
    except:
        messages.error(request, _('Профиль барбера не найден.'))
        return redirect('accounts:dashboard')

    # Получаем или создаем настройки расписания
    try:
        settings = barber_profile.schedule_settings
    except BarberScheduleSettings.DoesNotExist:
        settings = None

    if request.method == 'POST':
        form = BarberScheduleSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            settings_obj = form.save(commit=False)
            settings_obj.barber = barber_profile
            settings_obj.save()

            messages.success(request, _('Настройки расписания сохранены!'))

            # Спросить, нужно ли сгенерировать слоты
            if 'generate_slots' in request.POST:
                generator = SlotGeneratorService(barber_profile)
                total_slots, message = generator.generate_slots_for_period()
                messages.success(request, message)

            return redirect('schedule:settings')
    else:
        form = BarberScheduleSettingsForm(instance=settings)

    context = {
        'form': form,
        'settings': settings,
        'title': 'Настройки расписания'
    }
    return render(request, 'schedule/settings.html', context)


@login_required
def calendar_view(request):
    """
    Календарь с слотами барбера.
    """
    if not request.user.is_barber:
        messages.error(request, _('Только барберы могут просматривать календарь.'))
        return redirect('accounts:dashboard')

    try:
        barber_profile = request.user.barber_profile
    except:
        messages.error(request, _('Профиль барбера не найден.'))
        return redirect('accounts:dashboard')

    # Получаем параметры из запроса
    year = int(request.GET.get('year', date.today().year))
    month = int(request.GET.get('month', date.today().month))

    # Создаем календарь на месяц
    cal = calendar.monthcalendar(year, month)

    # Получаем слоты на этот месяц
    first_day = date(year, month, 1)
    if month == 12:
        last_day = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(year, month + 1, 1) - timedelta(days=1)

    slots = TimeSlot.objects.filter(
        barber=barber_profile,
        date__gte=first_day,
        date__lte=last_day
    ).select_related('booking')

    # Группируем слоты по датам
    slots_by_date = {}
    for slot in slots:
        if slot.date not in slots_by_date:
            slots_by_date[slot.date] = {
                'available': 0,
                'booked': 0,
                'blocked': 0
            }
        slots_by_date[slot.date][slot.status] += 1

    # Получаем переопределения на этот месяц
    overrides = ScheduleOverride.objects.filter(
        barber=barber_profile,
        date__gte=first_day,
        date__lte=last_day
    )
    overrides_by_date = {o.date: o for o in overrides}

    # Навигация по месяцам
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year

    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year

    context = {
        'title': 'Календарь слотов',
        'calendar': cal,
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'slots_by_date': slots_by_date,
        'overrides_by_date': overrides_by_date,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'today': date.today()
    }
    return render(request, 'schedule/calendar.html', context)


@login_required
def day_slots_view(request, year, month, day):
    """
    Просмотр и управление слотами конкретного дня.
    """
    if not request.user.is_barber:
        messages.error(request, _('Только барберы могут управлять слотами.'))
        return redirect('accounts:dashboard')

    try:
        barber_profile = request.user.barber_profile
    except:
        messages.error(request, _('Профиль барбера не найден.'))
        return redirect('accounts:dashboard')

    target_date = date(year, month, day)

    # Получаем слоты на этот день
    slots = TimeSlot.objects.filter(
        barber=barber_profile,
        date=target_date
    ).select_related('booking').order_by('start_time')

    # Получаем переопределение для этого дня (если есть)
    try:
        override = ScheduleOverride.objects.get(
            barber=barber_profile,
            date=target_date
        )
    except ScheduleOverride.DoesNotExist:
        override = None

    # Обработка действий
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'generate_slots':
            generator = SlotGeneratorService(barber_profile)
            total_slots, message = generator.generate_slots_for_date(target_date)
            messages.success(request, message)
            return redirect('schedule:day_slots', year=year, month=month, day=day)

        elif action == 'block_slot':
            slot_id = request.POST.get('slot_id')
            slot = get_object_or_404(TimeSlot, id=slot_id, barber=barber_profile)
            if slot.status == 'available':
                slot.status = 'blocked'
                slot.save()
                messages.success(request, _('Слот заблокирован.'))
            return redirect('schedule:day_slots', year=year, month=month, day=day)

        elif action == 'unblock_slot':
            slot_id = request.POST.get('slot_id')
            slot = get_object_or_404(TimeSlot, id=slot_id, barber=barber_profile)
            if slot.status == 'blocked' and not slot.booking:
                slot.status = 'available'
                slot.save()
                messages.success(request, _('Слот разблокирован.'))
            return redirect('schedule:day_slots', year=year, month=month, day=day)

    context = {
        'title': f'Слоты на {target_date.strftime("%d.%m.%Y")}',
        'target_date': target_date,
        'slots': slots,
        'override': override,
        'year': year,
        'month': month,
        'day': day
    }
    return render(request, 'schedule/day_slots.html', context)


@login_required
def override_create_view(request, year, month, day):
    """
    Создание исключения в расписании для конкретного дня.
    """
    if not request.user.is_barber:
        messages.error(request, _('Только барберы могут управлять расписанием.'))
        return redirect('accounts:dashboard')

    try:
        barber_profile = request.user.barber_profile
    except:
        messages.error(request, _('Профиль барбера не найден.'))
        return redirect('accounts:dashboard')

    target_date = date(year, month, day)

    # Проверяем, есть ли уже переопределение для этого дня
    try:
        override = ScheduleOverride.objects.get(
            barber=barber_profile,
            date=target_date
        )
        # Если есть, перенаправляем на редактирование
        return redirect('schedule:override_edit', override_id=override.id)
    except ScheduleOverride.DoesNotExist:
        override = None

    if request.method == 'POST':
        form = ScheduleOverrideForm(request.POST)
        if form.is_valid():
            override_obj = form.save(commit=False)
            override_obj.barber = barber_profile
            override_obj.date = target_date
            override_obj.save()

            messages.success(request, _('Исключение создано!'))
            return redirect('schedule:day_slots', year=year, month=month, day=day)
    else:
        form = ScheduleOverrideForm(initial={'date': target_date})

    context = {
        'form': form,
        'title': f'Создать исключение для {target_date.strftime("%d.%m.%Y")}',
        'target_date': target_date,
        'year': year,
        'month': month,
        'day': day
    }
    return render(request, 'schedule/override_form.html', context)


@login_required
def override_edit_view(request, override_id):
    """
    Редактирование исключения в расписании.
    """
    if not request.user.is_barber:
        messages.error(request, _('Только барберы могут управлять расписанием.'))
        return redirect('accounts:dashboard')

    try:
        barber_profile = request.user.barber_profile
    except:
        messages.error(request, _('Профиль барбера не найден.'))
        return redirect('accounts:dashboard')

    override = get_object_or_404(
        ScheduleOverride,
        id=override_id,
        barber=barber_profile
    )

    if request.method == 'POST':
        if 'delete' in request.POST:
            target_date = override.date
            override.delete()
            messages.success(request, _('Исключение удалено!'))
            return redirect('schedule:day_slots',
                          year=target_date.year,
                          month=target_date.month,
                          day=target_date.day)

        form = ScheduleOverrideForm(request.POST, instance=override)
        if form.is_valid():
            form.save()
            messages.success(request, _('Исключение обновлено!'))
            return redirect('schedule:day_slots',
                          year=override.date.year,
                          month=override.date.month,
                          day=override.date.day)
    else:
        form = ScheduleOverrideForm(instance=override)

    context = {
        'form': form,
        'override': override,
        'title': f'Редактировать исключение для {override.date.strftime("%d.%m.%Y")}'
    }
    return render(request, 'schedule/override_form.html', context)


@login_required
def bookings_view(request):
    """
    Список всех бронирований барбера.
    """
    if not request.user.is_barber:
        messages.error(request, _('Только барберы могут просматривать бронирования.'))
        return redirect('accounts:dashboard')

    try:
        barber_profile = request.user.barber_profile
    except:
        messages.error(request, _('Профиль барбера не найден.'))
        return redirect('accounts:dashboard')

    # Фильтры
    status_filter = request.GET.get('status', 'all')
    date_filter = request.GET.get('date', 'upcoming')

    bookings = Booking.objects.filter(barber=barber_profile)

    # Фильтр по статусу
    if status_filter != 'all':
        bookings = bookings.filter(status=status_filter)

    # Фильтр по дате
    if date_filter == 'upcoming':
        bookings = bookings.filter(booking_date__gte=date.today())
    elif date_filter == 'past':
        bookings = bookings.filter(booking_date__lt=date.today())
    elif date_filter == 'today':
        bookings = bookings.filter(booking_date=date.today())

    bookings = bookings.order_by('-booking_date', '-booking_start_time')

    context = {
        'title': 'Мои бронирования',
        'bookings': bookings,
        'status_filter': status_filter,
        'date_filter': date_filter
    }
    return render(request, 'schedule/bookings.html', context)
