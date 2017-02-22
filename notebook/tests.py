import json
from itertools import cycle

from django.http import JsonResponse
from django.test import TestCase
from django.urls import reverse_lazy
from model_mommy import mommy

from notebook.mommy_recipes import create_multiple_doctors
from reservation.models import Office

class DoctorDetialApiTest(TestCase):
    def setUp(self):
        self.doctor = create_multiple_doctors(1)[0]

    def test_api_status(self):
        response = self.client.get(reverse_lazy('react_doctor_detail', args=[self.doctor.id]))
        self.assertEqual(response.status_code, 200)

    def test_api_result(self):
        response = self.client.get(reverse_lazy('react_doctor_detail', args=[self.doctor.id]))
        self.assertEqual(response.status_code, 200)

        body_unicode = response.content.decode('utf-8')
        doctor_json = json.loads(body_unicode)
        self.assertEqual(doctor_json['id'], self.doctor.id)

class DoctorsApiTest(TestCase):
    DOCTOR_QUANTITY = 7

    def setUp(self):
        self.doctors = create_multiple_doctors(DoctorsApiTest.DOCTOR_QUANTITY)


    def test_api_status(self):
        response = self.client.get(reverse_lazy('react_doctors'))
        self.assertEqual(response.status_code, 200)

    def test_api_result(self):
        response = self.client.get(reverse_lazy('react_doctors'))
        self.assertEqual(response.status_code, 200)

        body_unicode = response.content.decode('utf-8')
        doctors_json = json.loads(body_unicode)
        self.assertEqual(len(doctors_json), DoctorsApiTest.DOCTOR_QUANTITY)
        for i in range(DoctorsApiTest.DOCTOR_QUANTITY):
            self.assertEqual(doctors_json[i]['id'], self.doctors[i].id)
