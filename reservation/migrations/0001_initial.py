# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-28 07:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailableTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('sat', 'شنبه'), ('sun', 'یک\u200cشنبه'), ('mon', 'دوشنبه'), ('tue', 'سه\u200cشنبه'), ('wed', 'چهارشنبه'), ('thu', 'پنج\u200cشنبه'), ('fri', 'جمعه')], default='شنبه', max_length=30)),
                ('range_num', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(choices=[('Tehran', 'تهران'), ('Isfahan', 'اصفهان'), ('Mahshad', 'مشهد'), ('Yazd', 'یزد'), ('Kerman', 'کرمان'), ('Rasht', 'رشت'), ('Zanjan', 'زنجان'), ('Qazvin', 'قزوین'), ('Qom', 'قم'), ('Hamedan', 'همدان'), ('Karaj', 'کرج')], default='تهران', max_length=30)),
                ('address', models.TextField()),
                ('phone', models.IntegerField()),
                ('telegram', models.CharField(max_length=30)),
                ('from_hour', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23)], null=True)),
                ('to_hour', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23)], null=True)),
                ('base_time', models.IntegerField(choices=[(10, '10'), (15, '15'), (20, '20'), (30, '30'), (60, '60')], default=15)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SystemUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_code', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='DoctorSecretary',
            fields=[
                ('role_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reservation.Role')),
            ],
            options={
                'abstract': False,
            },
            bases=('reservation.role',),
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('role_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reservation.Role')),
            ],
            options={
                'abstract': False,
            },
            bases=('reservation.role',),
        ),
        migrations.AddField(
            model_name='systemuser',
            name='role',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_role', to='reservation.Role'),
        ),
        migrations.AddField(
            model_name='systemuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='system_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='role',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_reservation.role_set+', to='contenttypes.ContentType'),
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('doctorsecretary_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reservation.DoctorSecretary')),
                ('doctor_code', models.PositiveIntegerField(default='')),
                ('education', models.CharField(choices=[('K', 'کارشناسی'), ('UK', 'کارشناسی\u200cارشد'), ('D', 'دکترا'), ('S', 'تخصص'), ('US', 'فوق تخصص')], max_length=30)),
                ('speciality', models.CharField(choices=[('Universal', 'عمومی'), ('Eye', 'چشم'), ('Zanan', 'زنان و زایمان و نازایی'), ('Jarahi', 'جراحی'), ('Govaresh', 'گوارش'), ('Poust', 'پوست، مو و زیبایی'), ('Kolie', 'کلیه و مجاری ادراری'), ('Maghz', 'مغز و اعصاب'), ('Ghalb', 'قلب و عروق'), ('Ghodad', 'غدد'), ('Goush', 'گوش و حلق و بینی'), ('Koudak', 'کودکان'), ('Dandan', 'دندان\u200cپزشکی'), ('Mama', 'مامایی'), ('Radio', 'رادیولوژی'), ('Sono', 'سونوگرافی')], max_length=30)),
                ('insurance', models.CharField(choices=[('Iran', 'ایران'), ('Asia', 'آسیا'), ('Tamin', 'سازمان تامین اجتماعی'), ('Salamat', 'جامع سلامت ایرانیان'), ('Mosalah', 'خدمات درمانی نیروهای مسلح و کارکنان دولت')], max_length=30)),
                ('price', models.PositiveIntegerField(default='')),
                ('cv', models.TextField(max_length=90)),
                ('contract', models.FileField(upload_to='contracts/')),
            ],
            options={
                'abstract': False,
            },
            bases=('reservation.doctorsecretary',),
        ),
        migrations.CreateModel(
            name='Secretary',
            fields=[
                ('doctorsecretary_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reservation.DoctorSecretary')),
            ],
            options={
                'abstract': False,
            },
            bases=('reservation.doctorsecretary',),
        ),
        migrations.AddField(
            model_name='doctorsecretary',
            name='office',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reservation.Office'),
        ),
        migrations.AddField(
            model_name='availabletime',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='available_times', to='reservation.Doctor'),
        ),
    ]
