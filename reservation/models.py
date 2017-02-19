import datetime
from abc import abstractmethod

import math
from distutils.log import Log

from django.db import models
from django.contrib.auth.models import User
from polymorphic.models import PolymorphicModel
from multiselectfield import MultiSelectField
from reservation import jalali


PATIENT_ROLE_ID = 1
DOCTOR_SECRETARY_ROLE_ID = 2
DOCTOR_ROLE_ID = 3
SECRETARY_ROLE_ID = 4

SATURDAY = 'sat'
SUNDAY = 'sun'
MONDAY = 'mon'
TUESDAY = 'tue'
WEDNESDAY = 'wed'
THURSDAY = 'thu'
FRIDAY = 'fri'


INSURANCE_TYPES = (
    ('Iran', 'ایران'),
    ('Asia', 'آسیا'),
    ('Tamin', 'سازمان تامین اجتماعی'),
    ('Salamat', 'جامع سلامت ایرانیان'),
    ('Mosalah', 'خدمات درمانی نیروهای مسلح و کارکنان دولت'),
    # TODO
)

SPECIALITY_TYPES = (
    ('Universal','عمومی'),
    ('Eye', 'چشم'),
    ('Zanan', 'زنان و زایمان و نازایی'),
    ('Jarahi', 'جراحی'),
    ('Govaresh', 'گوارش'),
    ('Poust', 'پوست، مو و زیبایی'),
    ('Kolie', 'کلیه و مجاری ادراری'),
    ('Maghz', 'مغز و اعصاب'),
    ('Ghalb', 'قلب و عروق'),
    ('Ghodad', 'غدد'),
    ('Goush', 'گوش و حلق و بینی'),
    ('Koudak', 'کودکان'),
    ('Dandan', 'دندان‌پزشکی'),
    ('Mama', 'مامایی'),
    ('Radio', 'رادیولوژی'),
    ('Sono', 'سونوگرافی')
    # TODO
)

EDUCATION_TYPES=(
    ('K', 'کارشناسی'),
    ('UK', 'کارشناسی‌ارشد'),
    ('D', 'دکترا'),
    ('S', 'متخصص'),
    ('US', 'فوق تخصص'),
)

CITY_NAMES=(
    ('Tehran', 'تهران'),
    ('Isfahan', 'اصفهان'),
    ('Mahshad', 'مشهد'),
    ('Yazd', 'یزد'),
    ('Kerman', 'کرمان'),
    ('Rasht', 'رشت'),
    ('Zanjan', 'زنجان'),
    ('Qazvin', 'قزوین'),
    ('Qom', 'قم'),
    ('Hamedan', 'همدان'),
    ('Karaj', 'کرج')

)

WEEK_DAYS = ((SATURDAY, 'شنبه'),
             (SUNDAY, 'یک‌شنبه'),
             (MONDAY, 'دوشنبه'),
             (TUESDAY, 'سه‌شنبه'),
             (WEDNESDAY, 'چهارشنبه'),
             (THURSDAY, 'پنج‌شنبه'),
             (FRIDAY, 'جمعه'))

BASE_TIMES = ((10, 10),
              (15, 15),
              (20, 20),
              (30, 30),
              (60, 60))

HOURS = [(i, i) for i in range(24)]

RESERVATION_STATUS = {
    'PENDING': 'در دست بررسی',
    'ACCEPTED': 'تعیین شده',
    'REJECTED': 'رد شده',
    'EXPIRED': 'تاریخ گذشته'
}



class Office(models.Model):
    # country = models.CharField(max_length=30, default='ایران')
    city = models.CharField("شهر",max_length=30, choices=CITY_NAMES, default='تهران', blank=True)
    address = models.TextField()
    phone = models.CharField(max_length=11, unique=True, null=True, blank=True,
                             error_messages={'unique': "این شماره تلفن برای مطب شخص دیگری ثبت شده‌است!"})
    telegram = models.CharField(max_length=30, null=True)
    from_hour = models.IntegerField("از ساعت", choices=HOURS, null=True, blank=True)   #TODO: RangeIntegerField create
    to_hour = models.IntegerField("تا ساعت", choices=HOURS, null=True, blank=True)
    base_time = models.IntegerField(choices=BASE_TIMES, default=15)
    opening_days = MultiSelectField(choices=WEEK_DAYS, null=True)

    lat_position = models.FloatField(null=True)
    lng_position = models.FloatField(null=True)

    @property
    def get_position(self):
        return str(self.lat_position) + ',' + str(self.lng_position)

    def get_base_time(self):
        return self.base_time

    def get_available_days(self):
        today = datetime.date.today()
        result, opening_days = [], []
        for day in self.opening_days:
            opening_days.append([x[0] for x in WEEK_DAYS].index(day))

        for i in range(14):
            day = today + datetime.timedelta(days=i)
            day_code = (day.weekday() + 2) % 7
            if day_code in opening_days:
                result.append((jalali.Gregorian(day).persian_string("{}/{}/{}"), WEEK_DAYS[day_code][1]))
        return result

    @property
    def doctor(self):
        doctor_secretary = self.doctorSecretary.all()
        for secretary in doctor_secretary:
            if secretary.get_role_id() == DOCTOR_ROLE_ID:
                return secretary

    def distance(self, lat, lng):
        return math.hypot(float(self.lat_position)-lat, float(self.lng_position)-lng)


class Role(PolymorphicModel):

    @abstractmethod
    def get_role_type(self):
        pass

    @abstractmethod
    def get_role_id(self):
        pass


class Patient(Role):
    def get_role_type(self):
        return "بیمار"

    def get_role_id(self):
        return PATIENT_ROLE_ID


class DoctorSecretary(Role):
    office = models.ForeignKey(Office, blank=True, null=True, related_name="doctorSecretary")

    def get_role_type(self):
        return "منشی پزشک"

    def get_role_id(self):
        return DOCTOR_SECRETARY_ROLE_ID

    def get_base_time(self):
        return self.office.get_base_time()

    @property
    def full_name(self):
        return self.user_role.full_name

    @property
    def username(self):
        return self.user_role.username

    @property
    def city(self):
        if self.office is not None:
            return self.office.get_city_display()
        return ''


class Doctor(DoctorSecretary):
    # doctor_secretary = models.OneToOneField(DoctorSecretary, related_name="doctor")
    doctor_code = models.PositiveIntegerField(default="", unique=True, error_messages={'unique': "این شماره نظام پزشکی برای پزشک دیگری ثبت شده است."})
    education = models.CharField(max_length=30,choices=EDUCATION_TYPES, blank=True)
    speciality = models.CharField(max_length=30,choices=SPECIALITY_TYPES, blank=True)
    insurance = models.CharField(max_length=30,choices=INSURANCE_TYPES, blank=True)
    price = models.PositiveIntegerField(default="", blank=True)
    cv = models.TextField(max_length=90, blank=True)
    contract = models.FileField(upload_to="contracts/")

    def get_role_type(self):
        return "پزشک"

    def get_role_id(self):
        return DOCTOR_ROLE_ID

    @property
    def full_name(self):
        return self.user_role.full_name


class Secretary(DoctorSecretary):
    def get_role_type(self):
        return "منشی"

    def get_role_id(self):
        return SECRETARY_ROLE_ID


class SystemUser(models.Model):
    user = models.OneToOneField(User, related_name="system_user")
    id_code = models.CharField(max_length=10, unique=True, default="")  # min_length=10
    role = models.OneToOneField(Role, related_name="user_role", null=True, blank=True)     # or make a dummy/patient role!

    @property
    def full_name(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

    @property
    def username(self):
        return self.user.username


    def get_reserve_times(self):
        return self.get_accepted_reserve_times() | self.get_pending_reserve_times() | self.get_rejected_reserve_times() | self.get_expired_reserve_times()


    def get_pending_reserve_times(self):
        return Reservation.objects.filter(range_num__isnull=True,
                                          date__gte=datetime.date.today(),
                                          patient=self,
                                          rejected=False)

    def get_accepted_reserve_times(self):
        return Reservation.objects.filter(range_num__isnull=False,
                                          rejected=False,
                                          patient=self)

    def get_rejected_reserve_times(self):
        return Reservation.objects.filter(rejected=True,
                                          patient=self)

    def get_expired_reserve_times(self):
        return Reservation.objects.filter(range_num__isnull=True,
                                          patient=self,
                                          date__lt=datetime.date.today())


class Reservation(models.Model):
    from_time = models.IntegerField(choices=HOURS)
    to_time = models.IntegerField(choices=HOURS)
    date = models.DateField()
    patient = models.ForeignKey(SystemUser, related_name='Reservations')
    doctor = models.ForeignKey(Doctor, related_name='Reservations')
    range_num = models.IntegerField(null=True)
    rejected = models.BooleanField(default=False)

    def get_available_times(self):
        start_range_num = self.get_num_by_start(max(self.from_time,self.doctor.office.from_hour))
        end_range_num = self.get_num_by_start(min(self.to_time,self.doctor.office.to_hour))
        result = range(start_range_num, end_range_num)

        reservations = Reservation.objects.filter(doctor=self.doctor, date=self.date, range_num__isnull=False, range_num__gte=start_range_num, range_num__lt=end_range_num)
        not_available = [reservation.range_num for reservation in reservations]

        available = [x for x in result if x not in not_available]
        return [{'range': self.get_range_by_num(x), 'range_num': x} for x in available]

    @property
    def get_jalali(self):
        return jalali.Gregorian(self.date).persian_string()

    @property
    def status(self):
        if self.rejected:
            return 'REJECTED'
        if self.range_num is not None:
            return 'ACCEPTED'
        if self.date >= datetime.date.today():
            return 'PENDING'
        return 'EXPIRED'

    def get_status_display(self):
        return RESERVATION_STATUS[self.status]

    #   TODO: TEST
    def get_range_by_num(self, num):
        if not num:
            return -1, -1
        base = self.doctor.get_base_time()
        start = datetime.time((num * base) // 60, (num * base) % 60).strftime("%H:%M")
        end = datetime.time((((num + 1) * base) // 60), (((num + 1) * base) % 60)).strftime("%H:%M")
        return start, end

    def get_range(self):
        return self.get_range_by_num(self.range_num)

    def get_num_by_start(self, hour, minute=0):
        if minute%self.doctor.get_base_time() > 0:
            return -1
        return (hour*60 + minute) // self.doctor.get_base_time()
