"""
$>@<K 4;O C?@02;5=8O @0A?8A0=85< 8 1@>=8@>20=8O<8.
"""

from django import forms
from django.utils.translation import gettext_lazy as _
from .models import BarberScheduleSettings, ScheduleOverride, TimeSlot, Booking


class BarberScheduleSettingsForm(forms.ModelForm):
    """$>@<0 4;O =0AB@>5: @0A?8A0=8O 10@15@0."""

    # >;O 4;O 2K1>@0 @01>G8E 4=59 =545;8
    monday = forms.BooleanField(required=False, label=_('>=545;L=8:'))
    tuesday = forms.BooleanField(required=False, label=_('B>@=8:'))
    wednesday = forms.BooleanField(required=False, label=_('!@540'))
    thursday = forms.BooleanField(required=False, label=_(''5B25@3'))
    friday = forms.BooleanField(required=False, label=_('OB=8F0'))
    saturday = forms.BooleanField(required=False, label=_('!C11>B0'))
    sunday = forms.BooleanField(required=False, label=_('>A:@5A5=L5'))

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
            'work_start_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'work_end_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'break_start_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'break_end_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'slot_duration_minutes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 15,
                'max': 240,
                'step': 5
            }),
            'booking_advance_days': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 90
            }),
            'min_booking_notice_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 72
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def __init__(self, *args, **kwargs):
        """=8F80;870F8O D>@<K A 70?>;=5=85< G5:1>:A>2 @01>G8E 4=59."""
        super().__init__(*args, **kwargs)

        # A;8 5ABL instance, 70?>;=O5< G5:1>:AK @01>G8E 4=59
        if self.instance and self.instance.pk:
            working_days = self.instance.working_weekdays or []
            weekday_fields = {
                0: 'monday',
                1: 'tuesday',
                2: 'wednesday',
                3: 'thursday',
                4: 'friday',
                5: 'saturday',
                6: 'sunday'
            }
            for day_num, field_name in weekday_fields.items():
                self.fields[field_name].initial = day_num in working_days

    def clean(self):
        """0;840F8O D>@<K."""
        cleaned_data = super().clean()

        # !>18@05< 2K1@0==K5 4=8 =545;8
        working_weekdays = []
        weekday_mapping = {
            'monday': 0,
            'tuesday': 1,
            'wednesday': 2,
            'thursday': 3,
            'friday': 4,
            'saturday': 5,
            'sunday': 6
        }

        for field_name, day_num in weekday_mapping.items():
            if cleaned_data.get(field_name):
                working_weekdays.append(day_num)

        if not working_weekdays:
            raise forms.ValidationError(
                _('K15@8B5 E>BO 1K >48= @01>G89 45=L.')
            )

        cleaned_data['working_weekdays'] = working_weekdays

        # 0;840F8O 2@5<5=8 @01>BK
        work_start = cleaned_data.get('work_start_time')
        work_end = cleaned_data.get('work_end_time')

        if work_start and work_end and work_start >= work_end:
            raise forms.ValidationError(
                _('@5<O >:>=G0=8O @01>BK 4>;6=> 1KBL ?>765 2@5<5=8 =0G0;0.')
            )

        # 0;840F8O ?5@5@K20
        break_start = cleaned_data.get('break_start_time')
        break_end = cleaned_data.get('break_end_time')

        if break_start and break_end:
            if break_start >= break_end:
                raise forms.ValidationError(
                    _('@5<O >:>=G0=8O ?5@5@K20 4>;6=> 1KBL ?>765 2@5<5=8 =0G0;0.')
                )
            if work_start and work_end:
                if break_start < work_start or break_end > work_end:
                    raise forms.ValidationError(
                        _('5@5@K2 4>;65= 1KBL 2 ?@545;0E @01>G53> 2@5<5=8.')
                    )

        return cleaned_data

    def save(self, commit=True):
        """!>E@0=5=85 D>@<K A >1=>2;5=85< @01>G8E 4=59."""
        instance = super().save(commit=False)
        instance.working_weekdays = self.cleaned_data['working_weekdays']

        if commit:
            instance.save()

        return instance


class ScheduleOverrideForm(forms.ModelForm):
    """$>@<0 4;O A>740=8O 8A:;NG5=89 2 @0A?8A0=88."""

    class Meta:
        model = ScheduleOverride
        fields = [
            'date',
            'override_type',
            'custom_start_time',
            'custom_end_time',
            'custom_break_start',
            'custom_break_end',
            'notes'
        ]
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'override_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'custom_start_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'custom_end_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'custom_break_start': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'custom_break_end': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            })
        }

    def clean(self):
        """0;840F8O D>@<K."""
        cleaned_data = super().clean()
        override_type = cleaned_data.get('override_type')

        # @>25@:0 4;O custom_hours
        if override_type == 'custom_hours':
            custom_start = cleaned_data.get('custom_start_time')
            custom_end = cleaned_data.get('custom_end_time')

            if not custom_start or not custom_end:
                raise forms.ValidationError(
                    _(';O 87<5=5==>3> 2@5<5=8 @01>BK C:068B5 2@5<O =0G0;0 8 >:>=G0=8O.')
                )

            if custom_start >= custom_end:
                raise forms.ValidationError(
                    _('@5<O >:>=G0=8O 4>;6=> 1KBL ?>765 2@5<5=8 =0G0;0.')
                )

        # @>25@:0 4;O custom_break
        if override_type == 'custom_break':
            custom_break_start = cleaned_data.get('custom_break_start')
            custom_break_end = cleaned_data.get('custom_break_end')

            if not custom_break_start or not custom_break_end:
                raise forms.ValidationError(
                    _(';O 87<5=5==>3> ?5@5@K20 C:068B5 2@5<O =0G0;0 8 >:>=G0=8O.')
                )

            if custom_break_start >= custom_break_end:
                raise forms.ValidationError(
                    _('@5<O >:>=G0=8O ?5@5@K20 4>;6=> 1KBL ?>765 2@5<5=8 =0G0;0.')
                )

        return cleaned_data


class BookingForm(forms.ModelForm):
    """$>@<0 4;O A>740=8O 1@>=8@>20=8O."""

    class Meta:
        model = Booking
        fields = [
            'client_name',
            'client_phone',
            'client_email',
            'booking_date',
            'booking_start_time',
            'booking_end_time',
            'service_description',
            'client_notes',
            'price'
        ]
        widgets = {
            'client_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '20= 20=>2'
            }),
            'client_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 123-45-67'
            }),
            'client_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com'
            }),
            'booking_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'booking_start_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'booking_end_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'service_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '?8A0=85 CA;C38'
            }),
            'client_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': '><<5=B0@88 :;85=B0'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '1000.00',
                'step': '0.01'
            })
        }

    def clean(self):
        """0;840F8O D>@<K."""
        cleaned_data = super().clean()

        booking_start = cleaned_data.get('booking_start_time')
        booking_end = cleaned_data.get('booking_end_time')

        if booking_start and booking_end and booking_start >= booking_end:
            raise forms.ValidationError(
                _('@5<O >:>=G0=8O 4>;6=> 1KBL ?>765 2@5<5=8 =0G0;0.')
            )

        return cleaned_data
