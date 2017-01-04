from django.test import TestCase
from django.urls import reverse_lazy

from reservation import models
from reservation.models import Doctor
from reservation.tests.test_utils import create_multiple_doctors


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
        data_12_13_3 = {
            'from_hour': 12,
            'to_hour': 13
        }
        data_15_12_error = {
            'from_hour': 15,
            'to_hour': 12
        }
        response = self.client.get(reverse_lazy('searchResult'), data_12_15_5)
        self.assertEqual(len(response.context['object_list']), 5)
        response = self.client.get(reverse_lazy('searchResult'), data_11_16_7)
        self.assertEqual(len(response.context['object_list']), 7)
        response = self.client.get(reverse_lazy('searchResult'), data_12_13_3)
        self.assertEqual(len(response.context['object_list']), 3)
        response = self.client.get(reverse_lazy('searchResult'), data_15_12_error)
        self.assertEqual(len(response.context['object_list']), 0)

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
