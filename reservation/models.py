from django.db import models
from django.contrib.auth.models import User


class SystemUser(models.Model):
    test = models.CharField(max_length=10, null=True)
    user = models.OneToOneField(User, related_name="system_user" )
    id_code = models.CharField(max_length=10,  default="")  # min_length=10

class Secretary:
    None

INSURANCE_TYPES = (
    ('Iran', 'ایران'),
    ('Asia', 'آسیا'),
    ('Tamin', 'سازمان تامین اجتماعی'),
    ('Salamat', 'جامع سلامت ایرانیان'),
    ('Mosalah', 'خدمات درمانی نیروهای مسلح و کارکنان دولت'),
    # TODO
)

SPECIALITY_TYPES = (
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
    ('Dandan', 'دندان‌پزشکی')
    # TODO
)

class Doctor(Secretary):
    doctor_code = models.PositiveIntegerField(max_length=6)
    education = models.TextField(max_length=30)
    speciality = models.TextField(choices=SPECIALITY_TYPES)
    insurance = models.TextField(choices=INSURANCE_TYPES)
    price = models.PositiveIntegerField
    cv = models.TextField(max_length=1000)
