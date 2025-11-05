"""
Сигналы для автоматического создания профиля барбера.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, BarberProfile


@receiver(post_save, sender=User)
def create_barber_profile(sender, instance, created, **kwargs):
    """
    Автоматически создает профиль барбера при создании пользователя с ролью BARBER.
    """
    if created and instance.role == User.Role.BARBER:
        BarberProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_barber_profile(sender, instance, **kwargs):
    """
    Сохраняет профиль барбера при сохранении пользователя.
    """
    if instance.role == User.Role.BARBER and hasattr(instance, 'barber_profile'):
        instance.barber_profile.save()
