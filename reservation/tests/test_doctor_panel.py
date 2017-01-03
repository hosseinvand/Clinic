from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy

from reservation.models import SystemUser, INSURANCE_TYPES, Doctor

def create_test_user(username, password):
    return User.objects.create_user(username=username, email='ahmad@gmail.com', password=password,
                             first_name='ahmad', last_name='ahmad')

def create_test_doctor(doctor_code, username, password):
    user = create_test_user(username=username, password=password)
    doctor = Doctor.objects.create(doctor_code=doctor_code, education='S', speciality='Jarahi', insurance='Iran', price=35000, cv='maybe not the best doc in the world but the happiest one :)', contract='contracts/')
    return SystemUser.objects.create(user=user, id_code='123456', role=doctor)

class OfficeAddTest(TestCase):
    def test_page_status_for_anonymous_user(self):
        self.client.logout()
        response = self.client.get(reverse_lazy('addClinic'))
        self.assertNotEqual(response.status_code, 200)