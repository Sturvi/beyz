"""
Management command 4;O 35=5@0F88 2@5<5==KE A;>B>2.
>65B 1KBL 70?CI5= 2@CG=CN 8;8 02B><0B8G5A:8 G5@57 cron/celery.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
import logging

from schedule.services.slot_generator import generate_slots_for_all_barbers
from accounts.models import BarberProfile

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = '5=5@0F8O 2@5<5==KE A;>B>2 4;O 10@15@>2'

    def add_arguments(self, parser):
        """>102;5=85 0@3C<5=B>2 :><0=4=>9 AB@>:8."""
        parser.add_argument(
            '--barber-id',
            type=int,
            help='ID 10@15@0 4;O 35=5@0F88 A;>B>2 (?> C<>;G0=8N - 2A5 10@15@K)'
        )
        parser.add_argument(
            '--date',
            type=str,
            help='0B0 4;O 35=5@0F88 A;>B>2 2 D>@<0B5 YYYY-MM-DD (?> C<>;G0=8N - A;54CNI89 4>ABC?=K9 45=L)'
        )
        parser.add_argument(
            '--days',
            type=int,
            help='>;8G5AB2> 4=59 4;O 35=5@0F88 A;>B>2 (?> C<>;G0=8N - 87 =0AB@>5: 10@15@0)'
        )
        parser.add_argument(
            '--next-day-only',
            action='store_true',
            help='5=5@8@>20BL A;>BK B>;L:> 4;O A;54CNI53> 4>ABC?=>3> 4=O (4;O 02B><0B8G5A:>3> 70?CA:0)'
        )

    def handle(self, *args, **options):
        """K?>;=5=85 :><0=4K."""
        barber_id = options.get('barber_id')
        target_date_str = options.get('date')
        days_count = options.get('days')
        next_day_only = options.get('next_day_only')

        # 0@A8=3 40BK
        target_date = None
        if target_date_str:
            try:
                target_date = date.fromisoformat(target_date_str)
            except ValueError:
                self.stdout.write(
                    self.style.ERROR(
                        f'525@=K9 D>@<0B 40BK: {target_date_str}. '
                        f'A?>;L7C9B5 D>@<0B YYYY-MM-DD'
                    )
                )
                return

        # A;8 C:070= :>=:@5B=K9 10@15@
        if barber_id:
            try:
                barber = BarberProfile.objects.get(id=barber_id)
                self.stdout.write(f'5=5@0F8O A;>B>2 4;O 10@15@0: {barber}')

                from schedule.services.slot_generator import SlotGeneratorService
                generator = SlotGeneratorService(barber)

                if next_day_only:
                    total_slots, message = generator.generate_next_day_slots()
                elif target_date:
                    if days_count:
                        total_slots, message = generator.generate_slots_for_period(
                            target_date,
                            days_count
                        )
                    else:
                        total_slots, message = generator.generate_slots_for_date(
                            target_date
                        )
                else:
                    total_slots, message = generator.generate_slots_for_period(
                        days_count=days_count
                    )

                self.stdout.write(self.style.SUCCESS(message))

            except BarberProfile.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'0@15@ A ID {barber_id} =5 =0945=')
                )
                return

        # 5=5@0F8O 4;O 2A5E 10@15@>2
        else:
            self.stdout.write('5=5@0F8O A;>B>2 4;O 2A5E 0:B82=KE 10@15@>2...')

            if next_day_only:
                # ;O 02B><0B8G5A:>3> 70?CA:0 :064CN ?>;=>GL
                target_date = None
                days_count = None

            results = generate_slots_for_all_barbers(
                target_date=target_date,
                days_count=days_count
            )

            # K2>4 @57C;LB0B>2
            total_created = sum(r['slots_created'] for r in results.values())

            self.stdout.write(self.style.SUCCESS(
                f'\n{"="*60}\n'
                f'5=5@0F8O A;>B>2 7025@H5=0!\n'
                f'1@01>B0=> 10@15@>2: {len(results)}\n'
                f'A53> A>740=> A;>B>2: {total_created}\n'
                f'{"="*60}\n'
            ))

            for barber_name, result in results.items():
                status_style = self.style.SUCCESS if result['slots_created'] > 0 else self.style.WARNING
                self.stdout.write(
                    status_style(f"  {barber_name}: {result['message']}")
                )
