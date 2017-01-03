from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy

from reservation import models
from reservation.models import SystemUser, INSURANCE_TYPES, Doctor, Office


def create_test_user(username, password, first_name='ahmad', last_name='ahmadi'):
    return User.objects.create_user(username=username, email='ahmad@gmail.com', password=password,
                                    first_name=first_name, last_name=last_name)


def create_test_doctor(doctor_code, username, password):
    user = create_test_user(username=username, password=password)
    doctor = Doctor.objects.create(doctor_code=doctor_code, education='S', speciality='Jarahi', insurance='Iran',
                                   price=35000, cv='maybe not the best doc in the world but the happiest one :)',
                                   contract='contracts/')
    return SystemUser.objects.create(user=user, id_code='123456', role=doctor)


def create_office(phone, city, from_hour, to_hour):
    office = Office.objects.create(city=city, from_hour=from_hour, to_hour=to_hour, address="address",
                                   phone=phone, telegram="telegram", base_time=15, opening_days=None)
    return office


def create_custom_test_doctor(city, from_hour, to_hour, doctor_code, username, password, education, speciality,
                              insurance, price, id_code, first_name, last_name):
    user = create_test_user(username=username, password=password, first_name=first_name, last_name=last_name)
    doctor = Doctor.objects.create(doctor_code=doctor_code, education=education, speciality=speciality,
                                   insurance=insurance,
                                   price=price, cv='maybe not the best doc in the world but the happiest one :)',
                                   contract='contracts/')
    office = create_office(phone=price, city=city, from_hour=from_hour, to_hour=to_hour)
    doctor.office = office
    doctor.save()
    return SystemUser.objects.create(user=user, id_code=id_code, role=doctor)


def create_multiple_doctors(count):
    doctors = []
    for i in range(count):
        education = models.EDUCATION_TYPES[i % len(models.EDUCATION_TYPES)][0]
        speciality = models.SPECIALITY_TYPES[i % len(models.SPECIALITY_TYPES)][0]
        insurance = models.INSURANCE_TYPES[i % len(models.INSURANCE_TYPES)][0]
        city = models.CITY_NAMES[i % len(models.CITY_NAMES)][0]
        from_hour = (i + 8) % len(models.HOURS)
        to_hour = (i + 3 + 8) % len(models.HOURS)
        doctors.append(
            create_custom_test_doctor(city=city, from_hour=from_hour, to_hour=to_hour, doctor_code=i * 10,
                                      username="doctor{}".format(i), password="password{}".format(i),
                                      education=education,
                                      speciality=speciality, insurance=insurance, price=i * 10000, id_code=i * 200,
                                      first_name="first_name{}".format(i), last_name="last_name{}".format(i)))
    return doctors


class SearchTest(TestCase):
    COUNT = 10

    def setUp(self):
        create_multiple_doctors(self.COUNT)

    def test_all_fields_are_empty(self):
        response = self.client.get(reverse_lazy('searchResult'), {})
        self.assertEqual(len(response.context['object_list']), self.COUNT)

    def test_from_hour(self):
        data_12_15_5 = {
            'from_hour': 12,
            'to_hour': 15
        }
        data_11_16_7 = {
            'from_hour': 11,
            'to_hour': 16
        }
        data_12_13_1 = {
            'from_hour': 12,
            'to_hour': 13
        }
        data_15_12_error = {
            'from_hour': 15,
            'to_hour': 12
        }
        response = self.client.get(reverse_lazy('searchResult'), data_12_15_5)
        self.assertTrue(len(response.context['object_list']), 5)
        response = self.client.get(reverse_lazy('searchResult'), data_11_16_7)
        self.assertTrue(len(response.context['object_list']), 7)
        response = self.client.get(reverse_lazy('searchResult'), data_12_13_1)
        self.assertTrue(len(response.context['object_list']), 1)
        response = self.client.get(reverse_lazy('searchResult'), data_15_12_error)
        self.assertTrue(len(response.context['object_list']), 0)

    def test_city(self):
        data = {
            'city': models.CITY_NAMES[0][0]
        }
        response = self.client.get(reverse_lazy('searchResult'), data)
        self.assertTrue(all(doctor.office.city == data['city'] for doctor in response.context['object_list']))

    def test_speciality(self):
        data = {
            'speciality': 'Eye'
        }
        response = self.client.get(reverse_lazy('searchResult'), data)
        self.assertTrue(all(doctor.speciality == data['speciality'] for doctor in response.context['object_list']))
        self.assertEqual(len(response.context['object_list']), len(Doctor.objects.filter(speciality=data['speciality'])))

    def test_education(self):
        data = {
            'education': 'S'
        }
        response = self.client.get(reverse_lazy('searchResult'), data)
        self.assertTrue(all(doctor.education == data['education'] for doctor in response.context['object_list']))
        self.assertEqual(len(response.context['object_list']), len(Doctor.objects.filter(education=data['education'])))

    def test_max_price(self):
        data_small_price = {
            'max_price': 500
        }
        data_medium_price = {
            'max_price': 50000
        }
        data_large_price = {
            'max_price': 100000
        }
        response = self.client.get(reverse_lazy('searchResult'), data_small_price)
        self.assertEqual(len(response.context['object_list']), 1)
        response = self.client.get(reverse_lazy('searchResult'), data_medium_price)
        self.assertEqual(len(response.context['object_list']), 6)
        self.assertTrue(all(doctor.price <= data_medium_price['max_price'] for doctor in response.context['object_list']))
        response = self.client.get(reverse_lazy('searchResult'), data_large_price)
        self.assertEqual(len(response.context['object_list']), 10)
        self.assertTrue(all(doctor.price <= data_large_price['max_price'] for doctor in response.context['object_list']))

    def test_multiple_word_name(self):
        data_single_name_1 = {
            'name': 'first',
        }
        data_single_name_2 = {
            'name': '1'
        }
        data_single_name_3 = {
            'name': 'last'
        }
        data_single_name_4 = {
            'name': 'name'
        }
        data_multi_name_1 = {
            'name': 'name 1'
        }
        data_multi_name_2 = {
            'name': 'name last'
        }
        data_multi_name_3 = {
            'name': 'name last first'
        }
        data_multi_name_4 = {
            'name': 'name last first {}'.format(self.COUNT + 10)
        }
        response = self.client.get(reverse_lazy('searchResult'), data_single_name_1)
        self.assertEqual(len(response.context['object_list']), self.COUNT)
        response = self.client.get(reverse_lazy('searchResult'), data_single_name_2)
        self.assertEqual(len(response.context['object_list']), 1)
        response = self.client.get(reverse_lazy('searchResult'), data_single_name_3)
        self.assertEqual(len(response.context['object_list']), self.COUNT)
        response = self.client.get(reverse_lazy('searchResult'), data_single_name_4)
        self.assertEqual(len(response.context['object_list']), self.COUNT)
        response = self.client.get(reverse_lazy('searchResult'), data_multi_name_1)
        self.assertEqual(len(response.context['object_list']), 1)
        response = self.client.get(reverse_lazy('searchResult'), data_multi_name_2)
        self.assertEqual(len(response.context['object_list']), self.COUNT)
        response = self.client.get(reverse_lazy('searchResult'), data_multi_name_3)
        self.assertEqual(len(response.context['object_list']), self.COUNT)
        response = self.client.get(reverse_lazy('searchResult'), data_multi_name_4)
        self.assertEqual(len(response.context['object_list']), 0)
