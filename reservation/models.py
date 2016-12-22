from django.db import models
from django.contrib.auth.models import User

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
    ('S','تخصص'),
    ('US','فوق تخصص'),
)


class Office(models.Model):
    country = models.CharField(max_length=30, default='ایران')
    city = models.CharField(max_length=30)
    address = models.TextField()
    phone = models.IntegerField()
    telegram = models.CharField(max_length=30)


class Role(models.Model):
    None


class Secretary(Role):
    office = models.ForeignKey(Office, related_name='secretaries', null=True, blank=True)


class Doctor(Secretary):
    # doctor_secretary = models.OneToOneField(Secretary, related_name="doctor")
    doctor_code = models.PositiveIntegerField(default="")
    education = models.CharField(max_length=30,choices=EDUCATION_TYPES)
    speciality = models.CharField(max_length=30,choices=SPECIALITY_TYPES)
    insurance = models.CharField(max_length=30,choices=INSURANCE_TYPES)
    price = models.PositiveIntegerField(default="")
    cv = models.TextField(max_length=90)
    contract = models.FileField(upload_to="contracts/")   #todo: give address where to go contract file!


class SystemUser(models.Model):
    user = models.OneToOneField(User, related_name="system_user")
    id_code = models.CharField(max_length=10,  default="")  # min_length=10
    role = models.ForeignKey(Role, related_name="user_role", null=True, blank=True)     # or make a dummy/patient role!
