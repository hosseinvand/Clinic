from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy
from reservation import models

from reservation.models import SystemUser, INSURANCE_TYPES, Doctor
from reservation.tests import test_utils


def create_test_user(username, password):
    return User.objects.create_user(username=username, email='ahmad@gmail.com', password=password,
                             first_name='ahmad', last_name='ahmad')

def create_test_doctor(doctor_code, username, password):
    user = create_test_user(username=username, password=password)
    doctor = Doctor.objects.create(doctor_code=doctor_code, education='S', speciality='Jarahi', insurance='Iran', price=35000, cv='maybe not the best doc in the world but the happiest one :)', contract='contracts/')
    return SystemUser.objects.create(user=user, id_code='0012435687', role=doctor)

class OfficeAddTest(TestCase):
    def test_page_status_for_anonymous_user(self):
        self.client.logout()
        response = self.client.get(reverse_lazy('addClinic'))
        self.assertNotEqual(response.status_code, 200)


class AvailableDaysTest(TestCase):
    def test_available_days_and_time_range(self):
        office_data = {
            'city': 'Zanjan',
            'address': 'میدان انقلاب',
            'phone': '0223344213',
            'telegram': 'ahmadClinic',
            'from_hour': 13,
            'to_hour': 18,
            'base_time': 15,
            'opening_days': ['sat','tue','wed']
        }
        doctor_user = test_utils.create_test_doctor(123,"0018032311","mahshid","pass")
        self.client.login(username='mahshid', password='pass')
        response = self.client.post(reverse_lazy('addClinic'), office_data)
        self.assertEqual(response.status_code, 302)
        role = doctor_user.role
        role.refresh_from_db()
        print(doctor_user.role.office)
        print("len:",len(doctor_user.role.office.opening_days))
        self.assertEqual(len(doctor_user.role.office.opening_days), 3)
        days = doctor_user.role.office.get_available_days()
        self.assertEqual(len(doctor_user.role.office.opening_days)*2, len(days))    #change if more than 2 week!!!!!!
