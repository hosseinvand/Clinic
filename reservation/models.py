from abc import abstractmethod
from django.db import models
from django.contrib.auth.models import User
from polymorphic.models import PolymorphicModel

PATIENT_ROLE_ID = 1
DOCTOR_SECRETARY_ROLE_ID = 2
DOCTOR_ROLE_ID = 3
SECRETARY_ROLE_ID = 4

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

WEEK_DAYS = (('sat', 'شنبه'),
              ('sun', 'یک‌شنبه'),
              ('mon', 'دوشنبه'),
              ('tue', 'سه‌شنبه'),
              ('wed', 'چهارشنبه'),
              ('thu', 'پنج‌شنبه'),
              ('fri','جمعه'))

BASE_TIMES = ((10, '۱۰'),
              (15, '۱۵'),
              (20, '۲۰'),
              (30, '۳۰'),
              (60, '۶۰'))

HOURS = [(i, i) for i in range(24)]

class Time():
    def __init__(self,hour,minute):
        self.hour = hour
        self.minute = minute

class Office(models.Model):
    # country = models.CharField(max_length=30, default='ایران')
    city = models.CharField(max_length=30,choices=CITY_NAMES, default='تهران')
    address = models.TextField()
    phone = models.CharField(max_length=11,unique=True,null=True)
    telegram = models.CharField(max_length=30,null=True)
    from_hour = models.IntegerField(choices=HOURS,null=True)   #TODO: RangeIntegerField create
    to_hour = models.IntegerField(choices=HOURS,null=True)
    base_time = models.IntegerField(choices=BASE_TIMES, default=15)

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
    education = models.CharField(max_length=30,choices=EDUCATION_TYPES)
    speciality = models.CharField(max_length=30,choices=SPECIALITY_TYPES)
    insurance = models.CharField(max_length=30,choices=INSURANCE_TYPES)
    price = models.PositiveIntegerField(default="")
    cv = models.TextField(max_length=90)
    contract = models.FileField(upload_to="contracts/")

    def get_role_type(self):
        return "پزشک"

    def get_role_id(self):
        return DOCTOR_ROLE_ID


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


class AvailableTime(models.Model):
    day = models.CharField(max_length=30,choices=WEEK_DAYS,default='شنبه')   #TODO: esme ruz ha bere tuye office
    range_num = models.IntegerField()
    doctor = models.ForeignKey(Doctor, related_name='available_times')

    def num_to_range(self, num):
        base = self.doctor.get_base_time()
        start = Time(((num-1)*base)//60, ((num-1)*base)%60)
        end = Time((num*base)//60, (num*base)%60)
        return start, end

