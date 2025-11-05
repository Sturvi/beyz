"""
Модели для управления пользователями и профилями барберов.
Использует кастомную модель User с авторизацией по email.
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Кастомный менеджер для модели User.
    Обеспечивает создание пользователей и суперпользователей.
    """

    def create_user(self, email, password=None, **extra_fields):
        """Создание обычного пользователя."""
        if not email:
            raise ValueError(_('Email обязателен для регистрации'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создание суперпользователя (администратора)."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', User.Role.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя.
    Использует email вместо username для авторизации.
    Поддерживает роли: ADMIN и BARBER.
    """

    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Администратор')
        BARBER = 'BARBER', _('Барбер')

    email = models.EmailField(
        _('Email адрес'),
        unique=True,
        error_messages={
            'unique': _('Пользователь с таким email уже существует.'),
        }
    )
    role = models.CharField(
        _('Роль'),
        max_length=10,
        choices=Role.choices,
        default=Role.BARBER
    )
    is_staff = models.BooleanField(
        _('Статус персонала'),
        default=False,
        help_text=_('Определяет, может ли пользователь войти в админ-панель.')
    )
    is_active = models.BooleanField(
        _('Активный'),
        default=True,
        help_text=_('Определяет, активен ли аккаунт пользователя.')
    )
    date_joined = models.DateTimeField(_('Дата регистрации'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        """Проверка, является ли пользователь администратором."""
        return self.role == self.Role.ADMIN

    @property
    def is_barber(self):
        """Проверка, является ли пользователь барбером."""
        return self.role == self.Role.BARBER


class BarberProfile(models.Model):
    """
    Профиль барбера с дополнительной информацией.
    Связь один-к-одному с моделью User.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='barber_profile',
        verbose_name=_('Пользователь')
    )
    first_name = models.CharField(_('Имя'), max_length=100)
    last_name = models.CharField(_('Фамилия'), max_length=100)
    phone = models.CharField(
        _('Телефон'),
        max_length=20,
        blank=True,
        null=True
    )
    bio = models.TextField(
        _('О себе'),
        blank=True,
        null=True,
        help_text=_('Краткая информация о барбере')
    )
    photo = models.ImageField(
        _('Фото'),
        upload_to='barber_photos/',
        blank=True,
        null=True
    )
    experience_years = models.PositiveIntegerField(
        _('Опыт работы (лет)'),
        default=0
    )
    specializations = models.TextField(
        _('Специализации'),
        blank=True,
        null=True,
        help_text=_('Укажите специализации через запятую')
    )
    is_available = models.BooleanField(
        _('Доступен для записи'),
        default=True
    )
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)

    class Meta:
        verbose_name = _('Профиль барбера')
        verbose_name_plural = _('Профили барберов')
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def full_name(self):
        """Полное имя барбера."""
        return f'{self.first_name} {self.last_name}'
