#  C:>2>4AB2> ?> 8A?>;L7>20=8N A8AB5<K C?@02;5=8O A;>B0<8

## 17>@

!8AB5<0 C?@02;5=8O A;>B0<8 ?>72>;O5B 10@15@0< C4>1=> =0AB@0820BL A2>5 @0A?8A0=85 @01>BK, 02B><0B8G5A:8 35=5@8@>20BL 2@5<5==K5 A;>BK 4;O 70?8A8 :;85=B>2 8 C?@02;OBL 1@>=8@>20=8O<8.

## A=>2=K5 2>7<>6=>AB8

### 1. 0AB@>9:8 @0A?8A0=8O

0@15@ <>65B =0AB@>8BL A2>5 @01>G55 @0A?8A0=85:
- ** 01>G85 4=8 =545;8** - 2K1>@ 4=59, :>340 10@15@ @01>B05B (?=-2A)
- **@5<O @01>BK** - =0G0;> 8 >:>=G0=85 @01>G53> 4=O
- **5@5@K2** - 2@5<O =0G0;0 8 >:>=G0=8O >1545==>3> ?5@5@K20
- **@>4>;68B5;L=>ABL A50=A0** - 4;8B5;L=>ABL >4=>3> A;>B0 (15-240 <8=CB)
- **5@8>4 >B:@KB8O 70?8A8** - =0 A:>;L:> 4=59 2?5@54 >B:@K205BAO 70?8AL (1-90 4=59)
- **8=8<0;L=>5 2@5<O C254><;5=8O** - 70 A:>;L:> G0A>2 <8=8<C< =C6=> 70?8AK20BLAO

### 2. 2B><0B8G5A:0O 35=5@0F8O A;>B>2

0 >A=>25 =0AB@>5: @0A?8A0=8O 02B><0B8G5A:8 A>740NBAO 2@5<5==K5 A;>BK:
- !;>BK 35=5@8@CNBAO A CG5B>< @01>G8E 4=59, 2@5<5=8 @01>BK 8 ?5@5@K2>2
- 064CN ?>;=>GL 02B><0B8G5A:8 A>740NBAO A;>BK 4;O A;54CNI53> 4>ABC?=>3> 4=O
- >6=> 2@CG=CN 35=5@8@>20BL A;>BK =0 ;N1>9 ?5@8>4

### 3. #?@02;5=85 8A:;NG5=8O<8

0@15@ <>65B A>74020BL 8A:;NG5=8O 4;O >B45;L=KE 4=59:
- **KE>4=>9 45=L** - >B<5B8BL 45=L :0: =5@01>G89
- **7<5=5=85 2@5<5=8 @01>BK** - C:070BL 4@C3>5 2@5<O @01>BK 4;O :>=:@5B=>3> 4=O
- **7<5=5=85 ?5@5@K20** - C:070BL 4@C3>5 2@5<O ?5@5@K20

### 4. #?@02;5=85 A;>B0<8

;O :064>3> 4=O <>6=>:
- @>A<0B@820BL 2A5 A;>BK
- ;>:8@>20BL/@071;>:8@>20BL A;>BK
- 5=5@8@>20BL =>2K5 A;>BK
- @>A<0B@820BL 1@>=8@>20=8O

## !B@C:BC@0 40==KE

### >45;8

1. **BarberScheduleSettings** - =0AB@>9:8 @0A?8A0=8O 10@15@0
   - `working_weekdays` - A?8A>: @01>G8E 4=59 (0=?=, 6=2A)
   - `work_start_time`, `work_end_time` - 2@5<O @01>BK
   - `break_start_time`, `break_end_time` - 2@5<O ?5@5@K20
   - `slot_duration_minutes` - ?@>4>;68B5;L=>ABL A;>B0
   - `booking_advance_days` - ?5@8>4 >B:@KB8O 70?8A8
   - `min_booking_notice_hours` - <8=8<0;L=>5 2@5<O C254><;5=8O
   - `is_active` - 0:B82=0 ;8 02B><0B8G5A:0O 35=5@0F8O

2. **ScheduleOverride** - 8A:;NG5=8O 2 @0A?8A0=88
   - `date` - 40B0 8A:;NG5=8O
   - `override_type` - B8? (2KE>4=>9/87<5=5=85 2@5<5=8/87<5=5=85 ?5@5@K20)
   - `custom_start_time`, `custom_end_time` - 87<5=5==>5 2@5<O @01>BK
   - `custom_break_start`, `custom_break_end` - 87<5=5==K9 ?5@5@K2

3. **TimeSlot** - 2@5<5==>9 A;>B
   - `date`, `start_time`, `end_time` - 40B0 8 2@5<O A;>B0
   - `status` - AB0BCA (available/booked/blocked)
   - `booking` - A2O7L A 1@>=8@>20=85<
   - `is_auto_generated` - 02B><0B8G5A:8 A35=5@8@>20= 8;8 A>740= 2@CG=CN

4. **Booking** - 1@>=8@>20=85
   - =D>@<0F8O > :;85=B5 (8<O, B5;5D>=, email)
   - 0B0 8 2@5<O 1@>=8@>20=8O
   - ?8A0=85 CA;C38, 70<5B:8
   - !B0BCA (pending/confirmed/cancelled/completed/no_show)
   - !B>8<>ABL

## A?>;L7>20=85

### 5@28G=0O =0AB@>9:0

1. >948B5 2 A8AB5<C :0: 10@15@
2. 5@5948B5 2 @0745; "0AB@>9:8 @0A?8A0=8O" (`/schedule/settings/`)
3. 0?>;=8B5 D>@<C:
   - K15@8B5 @01>G85 4=8 =545;8
   - #:068B5 2@5<O @01>BK
   - #:068B5 2@5<O ?5@5@K20 (>?F8>=0;L=>)
   - #AB0=>28B5 ?@>4>;68B5;L=>ABL A50=A0 (=0?@8<5@, 30 <8=CB)
   - #:068B5 ?5@8>4 >B:@KB8O 70?8A8 (=0?@8<5@, 14 4=59)
4. !>E@0=8B5 =0AB@>9:8
5. ?F8>=0;L=>: A@07C A35=5@8@C9B5 A;>BK =0 25AL ?5@8>4

### Management :><0=4K

#### 5=5@0F8O A;>B>2

```bash
# !35=5@8@>20BL A;>BK 4;O 2A5E 10@15@>2 (A;54CNI89 4>ABC?=K9 45=L)
python manage.py generate_slots --next-day-only

# !35=5@8@>20BL A;>BK 4;O :>=:@5B=>3> 10@15@0
python manage.py generate_slots --barber-id=1

# !35=5@8@>20BL A;>BK =0 :>=:@5B=CN 40BC
python manage.py generate_slots --date=2025-11-10

# !35=5@8@>20BL A;>BK =0 ?5@8>4 (=0?@8<5@, 30 4=59)
python manage.py generate_slots --days=30

# !35=5@8@>20BL A;>BK 4;O 10@15@0 =0 :>=:@5B=CN 40BC 8 ?5@8>4
python manage.py generate_slots --barber-id=1 --date=2025-11-10 --days=7
```

### 2B><0B8G5A:0O 35=5@0F8O A;>B>2 (Cron)

'B>1K 02B><0B8G5A:8 35=5@8@>20BL A;>BK :064CN ?>;=>GL, 4>102LB5 2 cron:

```bash
#  540:B8@>20BL crontab
crontab -e

# >1028BL AB@>:C (35=5@0F8O A;>B>2 :064CN ?>;=>GL)
0 0 * * * cd /path/to/project && python manage.py generate_slots --next-day-only
```

;8 8A?>;L7C9B5 systemd timer, 8;8 ;N1>9 4@C3>9 ?;0=8@>2I8: 7040G.

### ;LB5@=0B820: Celery Beat (>?F8>=0;L=>)

A;8 2 ?@>5:B5 8A?>;L7C5BAO Celery, <>6=> =0AB@>8BL ?5@8>48G5A:CN 7040GC:

```python
# config/celery.py
from celery import Celery
from celery.schedules import crontab

app = Celery('barber_booking')

app.conf.beat_schedule = {
    'generate-slots-midnight': {
        'task': 'schedule.tasks.generate_daily_slots',
        'schedule': crontab(hour=0, minute=0),  # 064CN ?>;=>GL
    },
}

# schedule/tasks.py
from celery import shared_task
from .services.slot_generator import generate_slots_for_all_barbers

@shared_task
def generate_daily_slots():
    """040G0 4;O 35=5@0F88 A;>B>2 :064CN ?>;=>GL."""
    results = generate_slots_for_all_barbers()
    return results
```

## URL <0@H@CBK

- `/schedule/settings/` - 0AB@>9:8 @0A?8A0=8O
- `/schedule/calendar/` - 0;5=40@L A> A;>B0<8
- `/schedule/day/<year>/<month>/<day>/` - !;>BK :>=:@5B=>3> 4=O
- `/schedule/override/create/<year>/<month>/<day>/` - !>740BL 8A:;NG5=85
- `/schedule/override/edit/<id>/` -  540:B8@>20BL 8A:;NG5=85
- `/schedule/bookings/` - !?8A>: 1@>=8@>20=89

## 4<8=8AB@0B82=0O ?0=5;L

 04<8=-?0=5;8 (`/admin/`) 4>ABC?=> C?@02;5=85 2A5<8 <>45;O<8:
- 0AB@>9:8 @0A?8A0=8O 10@15@>2
- A:;NG5=8O 2 @0A?8A0=88
- @5<5==K5 A;>BK
- @>=8@>20=8O

### 0AA>2K5 459AB28O 2 04<8=:5

- **!;>BK**: 1;>:8@>2:0/@071;>:8@>2:0 2K1@0==KE A;>B>2
- **@>=8@>20=8O**: ?>4B25@645=85/>B<5=0/7025@H5=85 2K1@0==KE 1@>=8@>20=89

## >38:0 @01>BK

### 5=5@0F8O A;>B>2

1. !8AB5<0 ?@>25@O5B =0AB@>9:8 @0A?8A0=8O 10@15@0
2. @>25@O5B, O2;O5BAO ;8 45=L @01>G8< (?> 45D>;B=K< =0AB@>9:0< 8;8 ?5@5>?@545;5=8N)
3. A;8 45=L 2KE>4=>9 - A;>BK =5 A>740NBAO
4. ?@545;O5B 2@5<O @01>BK A CG5B>< ?5@5>?@545;5=89
5. 5=5@8@C5B A;>BK A CG5B><:
   - @>4>;68B5;L=>AB8 A50=A0
   - @5<5=8 ?5@5@K20 (A;>BK =5 A>740NBAO 2> 2@5<O ?5@5@K20)
   - !CI5AB2CNI8E A;>B>2 (=5 4C1;8@C5B)
6. !B0@K5 02B><0B8G5A:8 A>740==K5 4>ABC?=K5 A;>BK C40;ONBAO 8 A>740NBAO 70=>2>

### !B0BCAK A;>B>2

- **available** - 4>ABC?5= 4;O 1@>=8@>20=8O
- **booked** - 701@>=8@>20= :;85=B><
- **blocked** - 701;>:8@>20= 10@15@>< 2@CG=CN

### !B0BCAK 1@>=8@>20=89

- **pending** - >68405B ?>4B25@645=8O
- **confirmed** - ?>4B25@645=>
- **cancelled** - >B<5=5=>
- **completed** - 7025@H5=>
- **no_show** - :;85=B =5 O28;AO

## @8<5@K 8A?>;L7>20=8O

### @8<5@ 1: !B0=40@B=>5 @0A?8A0=85

0@15@ @01>B05B ?=-?B A 9:00 4> 18:00, ?5@5@K2 13:00-14:00, A50=A 30 <8=CB:

```
0AB@>9:8:
-  01>G85 4=8: ?=, 2B, A@, GB, ?B (0, 1, 2, 3, 4)
- @5<O @01>BK: 09:00 - 18:00
- 5@5@K2: 13:00 - 14:00
- @>4>;68B5;L=>ABL A50=A0: 30 <8=CB
- 5@8>4 >B:@KB8O 70?8A8: 14 4=59

 57C;LB0B:
0 :064K9 @01>G89 45=L A>740NBAO A;>BK:
09:00-09:30, 09:30-10:00, ..., 12:30-13:00 (?5@5@K2), 14:00-14:30, ..., 17:30-18:00
```

### @8<5@ 2: A:;NG5=85 - 2KE>4=>9

0@15@ E>G5B 27OBL 2KE>4=>9 15 =>O1@O:

```
59AB28O:
1. 5@59B8 2 :0;5=40@L
2. K1@0BL 15 =>O1@O
3. !>740BL 8A:;NG5=85: "KE>4=>9 45=L"

 57C;LB0B:
!;>BK =0 15 =>O1@O =5 1C4CB A>740=K, ACI5AB2CNI85 4>ABC?=K5 A;>BK C40;5=K
```

### @8<5@ 3: A:;NG5=85 - 87<5=5=85 2@5<5=8 @01>BK

0@15@ 20 =>O1@O @01>B05B A 10:00 4> 16:00:

```
59AB28O:
1. 5@59B8 2 :0;5=40@L
2. K1@0BL 20 =>O1@O
3. !>740BL 8A:;NG5=85: "7<5=5=85 2@5<5=8 @01>BK"
4. #:070BL: 10:00 - 16:00

 57C;LB0B:
0 20 =>O1@O A;>BK 1C4CB A>740=K A 10:00 4> 16:00 2<5AB> AB0=40@B=>3> 2@5<5=8
```

## 0;L=59H55 @0728B85

### ;0=8@C5BAO 4>1028BL:

1. **UI H01;>=K** - 3>B>2K5 HTML H01;>=K 4;O 2A5E AB@0=8F
2. **API 4;O :;85=B>2** - REST API 4;O 1@>=8@>20=8O A;>B>2 :;85=B0<8
3. **#254><;5=8O** - email/SMS C254><;5=8O > 1@>=8@>20=8OE
4. **=B53@0F8O A :0;5=40@O<8** - M:A?>@B 2 Google Calendar, iCal
5. **!B0B8AB8:0** - 0=0;8B8:0 ?> 1@>=8@>20=8O< 8 703@C65==>AB8
6. **=>65AB25==K5 CA;C38** - @07=K5 CA;C38 A @07=>9 ?@>4>;68B5;L=>ABLN
7. **=;09=->?;0B0** - 8=B53@0F8O A ?;0B56=K<8 A8AB5<0<8

## >445@6:0

@8 2>7=8:=>25=88 2>?@>A>2 8;8 ?@>1;5<:
1. @>25@LB5 ;>38 Django
2. #1548B5AL, GB> 2A5 <83@0F88 ?@8<5=5=K
3. @>25@LB5 =0AB@>9:8 @0A?8A0=8O 2 04<8=-?0=5;8
