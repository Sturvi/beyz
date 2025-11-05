"""
Views для аутентификации и управления профилями.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .forms import UserLoginForm, BarberProfileForm
from .models import BarberProfile


def login_view(request):
    """
    Страница авторизации пользователей.
    """
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, _(f'Добро пожаловать, {user.email}!'))
            return redirect('accounts:dashboard')
    else:
        form = UserLoginForm()

    context = {
        'form': form,
        'title': 'Вход в систему'
    }
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    """
    Выход из системы.
    """
    logout(request)
    messages.info(request, _('Вы успешно вышли из системы.'))
    return redirect('accounts:login')


@login_required
def dashboard_view(request):
    """
    Главная страница после авторизации (дашборд).
    """
    context = {
        'title': 'Панель управления',
        'user': request.user
    }

    # Если пользователь - барбер, получаем его профиль
    if request.user.is_barber:
        try:
            context['barber_profile'] = request.user.barber_profile
        except BarberProfile.DoesNotExist:
            # Создаем профиль, если его нет
            BarberProfile.objects.create(user=request.user)
            context['barber_profile'] = request.user.barber_profile

    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile_view(request):
    """
    Страница профиля барбера.
    """
    if not request.user.is_barber:
        messages.error(request, _('Только барберы могут редактировать профиль.'))
        return redirect('accounts:dashboard')

    try:
        barber_profile = request.user.barber_profile
    except BarberProfile.DoesNotExist:
        barber_profile = BarberProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = BarberProfileForm(request.POST, request.FILES, instance=barber_profile)
        if form.is_valid():
            form.save()
            messages.success(request, _('Профиль успешно обновлен!'))
            return redirect('accounts:profile')
    else:
        form = BarberProfileForm(instance=barber_profile)

    context = {
        'form': form,
        'title': 'Мой профиль',
        'barber_profile': barber_profile
    }
    return render(request, 'accounts/profile.html', context)
