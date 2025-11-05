"""
!5@28A 4;O 35=5@0F88 2@5<5==KE A;>B>2 4;O 10@15@>2.
"""

from datetime import datetime, date, time, timedelta
from typing import List, Optional, Tuple
from django.db import transaction
from django.utils import timezone
import logging

from ..models import (
    BarberScheduleSettings,
    ScheduleOverride,
    TimeSlot,
    BarberProfile
)

logger = logging.getLogger(__name__)


class SlotGeneratorService:
    """!5@28A 4;O 02B><0B8G5A:>9 35=5@0F88 2@5<5==KE A;>B>2."""

    def __init__(self, barber: BarberProfile):
        """
        =8F80;870F8O A5@28A0.

        Args:
            barber: @>D8;L 10@15@0, 4;O :>B>@>3> 35=5@8@CNBAO A;>BK
        """
        self.barber = barber
        try:
            self.settings = barber.schedule_settings
        except BarberScheduleSettings.DoesNotExist:
            self.settings = None

    def generate_slots_for_date(self, target_date: date) -> Tuple[int, str]:
        """
        5=5@0F8O A;>B>2 4;O :>=:@5B=>9 40BK.

        Args:
            target_date: 0B0, 4;O :>B>@>9 35=5@8@CNBAO A;>BK

        Returns:
            Tuple[int, str]: >;8G5AB2> A>740==KE A;>B>2 8 A>>1I5=85
        """
        if not self.settings or not self.settings.is_active:
            return 0, f'0AB@>9:8 @0A?8A0=8O =5 0:B82=K 4;O {self.barber}'

        # 5 35=5@8@C5< A;>BK 4;O ?@>H54H8E 40B
        if target_date < date.today():
            return 0, f'0B0 {target_date} C65 ?@>H;0'

        # @>25@O5<, 5ABL ;8 ?5@5>?@545;5=85 4;O MB>9 40BK
        override = self._get_override_for_date(target_date)

        # A;8 45=L 2KE>4=>9, =5 35=5@8@C5< A;>BK
        if override and override.override_type == 'day_off':
            logger.info(f'5=L {target_date} >B<5G5= :0: 2KE>4=>9 4;O {self.barber}')
            return 0, f'5=L {target_date} - 2KE>4=>9'

        # @>25@O5<, @01>G89 ;8 MB> 45=L ?> C<>;G0=8N
        if not self.settings.is_working_day(target_date) and not override:
            logger.info(f'5=L {target_date} =5 O2;O5BAO @01>G8< 4;O {self.barber}')
            return 0, f'5=L {target_date} - =5@01>G89'

        # ?@545;O5< 2@5<O @01>BK A CG5B>< ?5@5>?@545;5=89
        work_start, work_end = self._get_working_hours(target_date, override)
        break_start, break_end = self._get_break_hours(target_date, override)

        # 5=5@8@C5< A;>BK
        slots_created = self._create_time_slots(
            target_date,
            work_start,
            work_end,
            break_start,
            break_end
        )

        return slots_created, f'!>740=> {slots_created} A;>B>2 4;O {target_date}'

    def generate_slots_for_period(
        self,
        start_date: Optional[date] = None,
        days_count: Optional[int] = None
    ) -> Tuple[int, str]:
        """
        5=5@0F8O A;>B>2 =0 ?5@8>4 2@5<5=8.

        Args:
            start_date: 0G0;L=0O 40B0 (?> C<>;G0=8N - A53>4=O)
            days_count: >;8G5AB2> 4=59 (?> C<>;G0=8N - 87 =0AB@>5: booking_advance_days)

        Returns:
            Tuple[int, str]: 1I55 :>;8G5AB2> A>740==KE A;>B>2 8 A>>1I5=85
        """
        if not self.settings:
            return 0, f'0AB@>9:8 @0A?8A0=8O =5 =0945=K 4;O {self.barber}'

        start_date = start_date or date.today()
        days_count = days_count or self.settings.booking_advance_days

        total_slots = 0
        messages = []

        for day_offset in range(days_count):
            target_date = start_date + timedelta(days=day_offset)
            slots_count, message = self.generate_slots_for_date(target_date)
            total_slots += slots_count
            if slots_count > 0:
                messages.append(message)

        summary = f'A53> A>740=> {total_slots} A;>B>2 =0 {days_count} 4=59'
        logger.info(summary)
        return total_slots, summary

    def generate_next_day_slots(self) -> Tuple[int, str]:
        """
        5=5@0F8O A;>B>2 4;O A;54CNI53> 4>ABC?=>3> 4=O.
        A?>;L7C5BAO 4;O 02B><0B8G5A:>3> 70?CA:0 :064CN ?>;=>GL.

        Returns:
            Tuple[int, str]: >;8G5AB2> A>740==KE A;>B>2 8 A>>1I5=85
        """
        if not self.settings:
            return 0, f'0AB@>9:8 @0A?8A0=8O =5 =0945=K 4;O {self.barber}'

        #  0AAG8BK205< 40BC =0 >A=>25 booking_advance_days
        target_date = date.today() + timedelta(days=self.settings.booking_advance_days)

        return self.generate_slots_for_date(target_date)

    def _get_override_for_date(self, target_date: date) -> Optional[ScheduleOverride]:
        """>;CG8BL ?5@5>?@545;5=85 @0A?8A0=8O 4;O 40BK."""
        try:
            return ScheduleOverride.objects.get(barber=self.barber, date=target_date)
        except ScheduleOverride.DoesNotExist:
            return None

    def _get_working_hours(
        self,
        target_date: date,
        override: Optional[ScheduleOverride]
    ) -> Tuple[time, time]:
        """
        >;CG8BL 2@5<O =0G0;0 8 >:>=G0=8O @01>BK.

        Args:
            target_date: &5;520O 40B0
            override: 5@5>?@545;5=85 @0A?8A0=8O (5A;8 5ABL)

        Returns:
            Tuple[time, time]: @5<O =0G0;0 8 >:>=G0=8O @01>BK
        """
        if override and override.override_type == 'custom_hours':
            return override.custom_start_time, override.custom_end_time

        return self.settings.work_start_time, self.settings.work_end_time

    def _get_break_hours(
        self,
        target_date: date,
        override: Optional[ScheduleOverride]
    ) -> Tuple[Optional[time], Optional[time]]:
        """
        >;CG8BL 2@5<O =0G0;0 8 >:>=G0=8O ?5@5@K20.

        Args:
            target_date: &5;520O 40B0
            override: 5@5>?@545;5=85 @0A?8A0=8O (5A;8 5ABL)

        Returns:
            Tuple[Optional[time], Optional[time]]: @5<O =0G0;0 8 >:>=G0=8O ?5@5@K20
        """
        if override and override.override_type == 'custom_break':
            return override.custom_break_start, override.custom_break_end

        return self.settings.break_start_time, self.settings.break_end_time

    def _create_time_slots(
        self,
        target_date: date,
        work_start: time,
        work_end: time,
        break_start: Optional[time],
        break_end: Optional[time]
    ) -> int:
        """
        !>740BL 2@5<5==K5 A;>BK 4;O 4=O.

        Args:
            target_date: 0B0
            work_start: @5<O =0G0;0 @01>BK
            work_end: @5<O >:>=G0=8O @01>BK
            break_start: @5<O =0G0;0 ?5@5@K20
            break_end: @5<O >:>=G0=8O ?5@5@K20

        Returns:
            int: >;8G5AB2> A>740==KE A;>B>2
        """
        slot_duration = timedelta(minutes=self.settings.slot_duration_minutes)

        # #40;O5< AB0@K5 02B><0B8G5A:8 A35=5@8@>20==K5 4>ABC?=K5 A;>BK 4;O MB>9 40BK
        TimeSlot.objects.filter(
            barber=self.barber,
            date=target_date,
            status='available',
            is_auto_generated=True
        ).delete()

        slots_to_create = []
        current_datetime = datetime.combine(target_date, work_start)
        end_datetime = datetime.combine(target_date, work_end)

        # >=25@B8@C5< ?5@5@K2 2 datetime 5A;8 >= 5ABL
        break_start_dt = datetime.combine(target_date, break_start) if break_start else None
        break_end_dt = datetime.combine(target_date, break_end) if break_end else None

        with transaction.atomic():
            while current_datetime + slot_duration <= end_datetime:
                slot_end = current_datetime + slot_duration

                # @>25@O5<, =5 ?>?0405B ;8 A;>B =0 2@5<O ?5@5@K20
                if break_start_dt and break_end_dt:
                    # A;8 A;>B =0G8=05BAO 8;8 70:0=G8205BAO 2> 2@5<O ?5@5@K20, ?@>?CA:05<
                    if (break_start_dt <= current_datetime < break_end_dt or
                        break_start_dt < slot_end <= break_end_dt):
                        current_datetime = slot_end
                        continue

                # @>25@O5<, ACI5AB2C5B ;8 C65 A;>B =0 MB> 2@5<O
                existing_slot = TimeSlot.objects.filter(
                    barber=self.barber,
                    date=target_date,
                    start_time=current_datetime.time()
                ).first()

                if not existing_slot:
                    slots_to_create.append(
                        TimeSlot(
                            barber=self.barber,
                            date=target_date,
                            start_time=current_datetime.time(),
                            end_time=slot_end.time(),
                            status='available',
                            is_auto_generated=True
                        )
                    )

                current_datetime = slot_end

            # 0AA>2>5 A>740=85 A;>B>2
            if slots_to_create:
                TimeSlot.objects.bulk_create(slots_to_create)
                logger.info(
                    f'!>740=> {len(slots_to_create)} A;>B>2 4;O {self.barber} '
                    f'=0 {target_date}'
                )

        return len(slots_to_create)


def generate_slots_for_all_barbers(
    target_date: Optional[date] = None,
    days_count: Optional[int] = None
) -> dict:
    """
    5=5@0F8O A;>B>2 4;O 2A5E 0:B82=KE 10@15@>2.

    Args:
        target_date: 0G0;L=0O 40B0 (?> C<>;G0=8N - A53>4=O)
        days_count: >;8G5AB2> 4=59 (?> C<>;G0=8N - 87 =0AB@>5: :064>3> 10@15@0)

    Returns:
        dict:  57C;LB0BK 35=5@0F88 4;O :064>3> 10@15@0
    """
    results = {}

    # >;CG05< 2A5E 10@15@>2 A 0:B82=K<8 =0AB@>9:0<8 @0A?8A0=8O
    barbers = BarberProfile.objects.filter(
        is_available=True,
        schedule_settings__is_active=True
    ).select_related('schedule_settings')

    for barber in barbers:
        generator = SlotGeneratorService(barber)

        if target_date is not None:
            if days_count:
                total_slots, message = generator.generate_slots_for_period(
                    target_date,
                    days_count
                )
            else:
                total_slots, message = generator.generate_slots_for_date(target_date)
        else:
            total_slots, message = generator.generate_next_day_slots()

        results[str(barber)] = {
            'slots_created': total_slots,
            'message': message
        }
        logger.info(f'{barber}: {message}')

    return results
