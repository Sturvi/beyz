"""
Формы для аутентификации и управления пользователями.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import User, BarberProfile


class UserLoginForm(AuthenticationForm):
    """
    Форма для авторизации пользователей через email.
    """

    username = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email@example.com',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label=_('Пароль'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '••••••••'
        })
    )

    error_messages = {
        'invalid_login': _(
            'Неверный email или пароль. Проверьте данные и попробуйте снова.'
        ),
        'inactive': _('Этот аккаунт неактивен.'),
    }


class UserRegistrationForm(UserCreationForm):
    """
    Форма для регистрации новых пользователей.
    """

    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email@example.com'
        })
    )
    password1 = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '••••••••'
        })
    )
    password2 = forms.CharField(
        label=_('Подтверждение пароля'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '••••••••'
        })
    )

    class Meta:
        model = User
        fields = ('email', 'role')
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'})
        }


class BarberProfileForm(forms.ModelForm):
    """
    Форма для редактирования профиля барбера.
    """

    class Meta:
        model = BarberProfile
        fields = (
            'first_name', 'last_name', 'phone', 'bio',
            'experience_years', 'specializations', 'photo', 'is_available'
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (999) 123-45-67'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Расскажите о себе...'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'specializations': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Стрижки, бритьё, окрашивание...'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
