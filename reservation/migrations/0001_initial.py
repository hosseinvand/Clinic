# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-21 06:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import reservation.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='SystemUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_code', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('role_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reservation.Role')),
            ],
            bases=('reservation.role',),
        ),
        migrations.CreateModel(
            name='Secretary',
            fields=[
                ('role_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reservation.Role')),
            ],
            bases=('reservation.role',),
        ),
        migrations.AddField(
            model_name='systemuser',
            name='role',
            field=models.ForeignKey(default=reservation.models.Patient, on_delete=django.db.models.deletion.CASCADE, related_name='user_role', to='reservation.Role'),
        ),
        migrations.AddField(
            model_name='systemuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='system_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('secretary_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reservation.Secretary')),
                ('doctor_code', models.PositiveIntegerField(max_length=6)),
                ('education', models.TextField(max_length=30)),
                ('speciality', models.TextField(choices=[('Eye', 'چشم'), ('Zanan', 'زنان و زایمان و نازایی'), ('Jarahi', 'جراحی'), ('Govaresh', 'گوارش'), ('Poust', 'پوست، مو و زیبایی'), ('Kolie', 'کلیه و مجاری ادراری'), ('Maghz', 'مغز و اعصاب'), ('Ghalb', 'قلب و عروق'), ('Ghodad', 'غدد'), ('Goush', 'گوش و حلق و بینی'), ('Koudak', 'کودکان'), ('Dandan', 'دندان\u200cپزشکی')])),
                ('insurance', models.TextField(choices=[('Iran', 'ایران'), ('Asia', 'آسیا'), ('Tamin', 'سازمان تامین اجتماعی'), ('Salamat', 'جامع سلامت ایرانیان'), ('Mosalah', 'خدمات درمانی نیروهای مسلح و کارکنان دولت')])),
                ('cv', models.TextField(max_length=1000)),
            ],
            bases=('reservation.secretary',),
        ),
    ]
