from abc import abstractmethod
from random import choice

from django.db import models
from django.contrib.auth.models import User
from polymorphic.models import PolymorphicModel
from multiselectfield import MultiSelectField

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
    ('K','کارشناسی'),
    ('UK','کارشناسی‌ارشد'),
    ('D','دکترا'),
    ('S','متخصص'),
    ('US','فوق تخصص'),
)

CITY_NAMES=(
    ('Tehran', 'تهران'),
    ('Isfahan', 'اصفهان'),
    ('Mahshad', 'مشهد'),
    ('Yazd', 'یزد'),
    ('Kerman','کرمان'),
    ('Rasht','رشت'),
    ('Zanjan','زنجان'),
    ('Qazvin','قزوین'),
    ('Qom','قم'),
    ('Hamedan','همدان'),
    ('Karaj','کرج')

)

WEEK_DAYS = ((SATURDAY, 'شنبه'),
             (SUNDAY, 'یک‌شنبه'),
             (MONDAY, 'دوشنبه'),
             (TUESDAY, 'سه‌شنبه'),
             (WEDNESDAY, 'چهارشنبه'),
             (THURSDAY, 'پنج‌شنبه'),
             (FRIDAY,'جمعه'))

BASE_TIMES = ((10, '۱۰'),
              (15, '۱۵'),
              (20, '۲۰'),
              (30, '۳۰'),
              (60, '۶۰'))

HOURS = [(i, i) for i in range(24)]

class Time:
    def __init__(self, hour, minute):
        self.hour = hour
        self.minute = minute

    def get_hour(self):
        return self.hour

    def get_minute(self):
        return self.minute

    def get_display_time(self):
        return '{} : {}'.format(self.hour, self.minute)

class Office(models.Model):
    # country = models.CharField(max_length=30, default='ایران')
    city = models.CharField(max_length=30,choices=CITY_NAMES, default='تهران',blank=True)
    address = models.TextField()
    phone = models.CharField(max_length=11,unique=True,null=True,blank=True)
    telegram = models.CharField(max_length=30,null=True)
    from_hour = models.IntegerField(choices=HOURS,null=True, blank=True)   #TODO: RangeIntegerField create
    to_hour = models.IntegerField(choices=HOURS,null=True, blank=True)
    base_time = models.IntegerField(choices=BASE_TIMES, default=15)
    opening_days = MultiSelectField(choices=WEEK_DAYS, null=True)

    def get_base_time(self):
        return self.base_time

class Role(PolymorphicModel):

    @abstractmethod
    def get_role_type(self):
        pass

    @abstractmethod
    def get_role_id(self):
        pass


class Patient(Role):

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(Patient, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            cls().save()
            return cls.objects.get()

    def get_role_type(self):
        return "بیمار"

    def get_role_id(self):
        return PATIENT_ROLE_ID


class DoctorSecretary(Role):
    office = models.ForeignKey(Office, blank=True, null=True)

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
    doctor_code = models.PositiveIntegerField(default="")
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



class ReserveTimeQuantity(models.Model):
    range_num = models.IntegerField()
    doctor = models.ForeignKey(Doctor, related_name='available_times')

    def get_range(self, num):
        base = self.doctor.get_base_time()
        start = Time(((num-1)*base)//60, ((num-1)*base)%60)
        end = Time((num*base)//60, (num*base)%60)
        return start, end

    def is_in_doctor_available_times(self):
        #TODO: check whether between start and end of doctor working hour or not
        pass