"""
URL :>=D83C@0F8O 4;O ?@8;>65=8O schedule.
"""

from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    # 0AB@>9:8 @0A?8A0=8O
    path('settings/', views.schedule_settings_view, name='settings'),

    # 0;5=40@L 8 A;>BK
    path('calendar/', views.calendar_view, name='calendar'),
    path('day/<int:year>/<int:month>/<int:day>/', views.day_slots_view, name='day_slots'),

    # A:;NG5=8O 2 @0A?8A0=88
    path('override/create/<int:year>/<int:month>/<int:day>/',
         views.override_create_view,
         name='override_create'),
    path('override/edit/<int:override_id>/',
         views.override_edit_view,
         name='override_edit'),

    # @>=8@>20=8O
    path('bookings/', views.bookings_view, name='bookings'),
]
