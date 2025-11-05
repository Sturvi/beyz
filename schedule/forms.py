"""
Forms for schedule and booking management.
"""

from django import forms
from django.utils.translation import gettext_lazy as _
from .models import BarberScheduleSettings, ScheduleOverride, TimeSlot, Booking


class BarberScheduleSettingsForm(forms.ModelForm):
    """Form for barber schedule settings."""

    # Fields for selecting working weekdays
    monday = forms.BooleanField(required=False, label='Monday')
    tuesday = forms.BooleanField(required=False, label='Tuesday')
    wednesday = forms.BooleanField(required=False, label='Wednesday')
    thursday = forms.BooleanField(required=False, label='Thursday')
    friday = forms.BooleanField(required=False, label='Friday')
    saturday = forms.BooleanField(required=False, label='Saturday')
    sunday = forms.BooleanField(required=False, label='Sunday')

    class Meta:
        model = BarberScheduleSettings
        fields = [
            'work_start_time',
            'work_end_time',
            'break_start_time',
            'break_end_time',
            'slot_duration_minutes',
            'booking_advance_days',
            'min_booking_notice_hours',
            'is_active'
        ]
        widgets = {
            'work_start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'work_end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'break_start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'break_end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'slot_duration_minutes': forms.NumberInput(attrs={'class': 'form-control', 'min': 15, 'max': 240, 'step': 5}),
            'booking_advance_days': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 90}),
            'min_booking_notice_hours': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 72}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def __init__(self, *args, **kwargs):
        """Initialize form with pre-filled working days checkboxes."""
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            working_days = self.instance.working_weekdays or []
            weekday_fields = {
                0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday',
                4: 'friday', 5: 'saturday', 6: 'sunday'
            }
            for day_num, field_name in weekday_fields.items():
                self.fields[field_name].initial = day_num in working_days

    def clean(self):
        """Validate form."""
        cleaned_data = super().clean()

        working_weekdays = []
        weekday_mapping = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
            'friday': 4, 'saturday': 5, 'sunday': 6
        }

        for field_name, day_num in weekday_mapping.items():
            if cleaned_data.get(field_name):
                working_weekdays.append(day_num)

        if not working_weekdays:
            raise forms.ValidationError('Please select at least one working day.')

        cleaned_data['working_weekdays'] = working_weekdays

        work_start = cleaned_data.get('work_start_time')
        work_end = cleaned_data.get('work_end_time')

        if work_start and work_end and work_start >= work_end:
            raise forms.ValidationError('End time must be after start time.')

        break_start = cleaned_data.get('break_start_time')
        break_end = cleaned_data.get('break_end_time')

        if break_start and break_end:
            if break_start >= break_end:
                raise forms.ValidationError('Break end time must be after break start time.')
            if work_start and work_end:
                if break_start < work_start or break_end > work_end:
                    raise forms.ValidationError('Break must be within working hours.')

        return cleaned_data

    def save(self, commit=True):
        """Save form with updated working days."""
        instance = super().save(commit=False)
        instance.working_weekdays = self.cleaned_data['working_weekdays']
        if commit:
            instance.save()
        return instance


class ScheduleOverrideForm(forms.ModelForm):
    """Form for creating schedule overrides."""

    class Meta:
        model = ScheduleOverride
        fields = [
            'date', 'override_type', 'custom_start_time', 'custom_end_time',
            'custom_break_start', 'custom_break_end', 'notes'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'override_type': forms.Select(attrs={'class': 'form-select'}),
            'custom_start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'custom_end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'custom_break_start': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'custom_break_end': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def clean(self):
        """Validate form."""
        cleaned_data = super().clean()
        override_type = cleaned_data.get('override_type')

        if override_type == 'custom_hours':
            custom_start = cleaned_data.get('custom_start_time')
            custom_end = cleaned_data.get('custom_end_time')

            if not custom_start or not custom_end:
                raise forms.ValidationError('Please specify start and end times for custom hours.')

            if custom_start >= custom_end:
                raise forms.ValidationError('End time must be after start time.')

        if override_type == 'custom_break':
            custom_break_start = cleaned_data.get('custom_break_start')
            custom_break_end = cleaned_data.get('custom_break_end')

            if not custom_break_start or not custom_break_end:
                raise forms.ValidationError('Please specify break start and end times.')

            if custom_break_start >= custom_break_end:
                raise forms.ValidationError('Break end time must be after break start time.')

        return cleaned_data


class BookingForm(forms.ModelForm):
    """Form for creating bookings."""

    class Meta:
        model = Booking
        fields = [
            'client_name', 'client_phone', 'client_email', 'booking_date',
            'booking_start_time', 'booking_end_time', 'service_description',
            'client_notes', 'price'
        ]
        widgets = {
            'client_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John Doe'}),
            'client_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 123-4567'}),
            'client_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'booking_start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'booking_end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'service_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Service description'}),
            'client_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Client notes'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '100.00', 'step': '0.01'})
        }

    def clean(self):
        """Validate form."""
        cleaned_data = super().clean()

        booking_start = cleaned_data.get('booking_start_time')
        booking_end = cleaned_data.get('booking_end_time')

        if booking_start and booking_end and booking_start >= booking_end:
            raise forms.ValidationError('End time must be after start time.')

        return cleaned_data
