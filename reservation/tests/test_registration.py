import os

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse_lazy

from reservation.models import SystemUser, INSURANCE_TYPES, Doctor, Office, Patient
from reservation.tests.test_utils import create_test_doctor, create_test_user, create_test_system_user


class OfficeAddTest(TestCase):
    def test_page_status_for_anonymous_user(self):
        self.client.logout()
        response = self.client.get(reverse_lazy('addClinic'))
        self.assertNotEqual(response.status_code, 200)

    def test_page_status_for_non_doctor_user(self):
        tmp_user = create_test_user(username='ahmad', password='password')
        patient = Patient()
        patient.save()
        SystemUser.objects.create(user=tmp_user, id_code='123456', role=patient)
        self.client.login(username='ahmad', password='password')
        response = self.client.get(reverse_lazy('addClinic'))
        self.assertNotEqual(response.status_code, 200)

    def test_add_new_offic(self):
        office_data = {
            'city': 'Zanjan',
            'address': 'میدان انقلاب',
            'phone': '0223344213',
            'telegram': 'ahmadClinic',
            'from_hour': '12',
            'to_hour': '15',
            'base_time': 15,
            'opening_days': 'sun'
        }
        doctor_system_user = create_test_doctor('123456', 'ahmad', 'password')
        self.client.login(username='ahmad', password='password')
        response = self.client.post(reverse_lazy('addClinic'), office_data)
        role = doctor_system_user.role
        role.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(role.office, Office.objects.get(phone=office_data['phone']))


class DoctorSignupViewTest(TestCase):
    doctor_data = {
        'doctor_code': 123456,
        'education': 'S',
        'speciality': 'Eye',
        'insurance': 'Iran',
        'price': 35000,
        'cv': 'test cv test cv',
        'contract': 'contracts/chi.jpg',
    }

    def setUp(self):
        upload_file = open(os.path.join(os.path.dirname(__file__), 'test_utils.py'), 'rb')
        self.doctor_data['contract'] = SimpleUploadedFile(upload_file.name, upload_file.read())

    def test_valid_new_doctor_creation(self):
        create_test_system_user(create_test_user(username='ahmad', password='password'), '0012332')
        self.client.login(username='ahmad', password='password')
        response = self.client.post(reverse_lazy('doctorRegister'), self.doctor_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Doctor.objects.filter(doctor_code=self.doctor_data['doctor_code']).exists())

    def test_invalid_new_doctor_code_already_exist(self):
        print(Doctor.objects.all())
        create_test_doctor(self.doctor_data['doctor_code'], 'doki', 'password')
        create_test_system_user(create_test_user('alien', 'alien'), '0052342')
        self.client.login(username='alien', password='alien')
        before_trying = len(Doctor.objects.all())
        response = self.client.post(reverse_lazy('doctorRegister'), self.doctor_data)
        after_trying = len(Doctor.objects.all())
        self.assertEqual(before_trying, after_trying)
        self.assertEqual(response.status_code, 200)



class LoginViewTest(TestCase):
    def test_page_status(self):
        response = self.client.get(reverse_lazy('login'))
        self.assertEqual(response.status_code, 200)

    def setUp(self):
        tmp_user = User.objects.create_user(username='ahmad', email='ahmad@gmail.com', password='password', first_name='ahmad',
                                            last_name='ahmad')
        SystemUser.objects.create(user=tmp_user, id_code='123456')


    def test_login_existing_user(self):
        login_data = {
            'username': 'ahmad',
            'password': 'password',
        }
        response = self.client.post(reverse_lazy('login'), login_data)
        self.assertEqual(response.status_code, 302)

    def test_login_existing_user_wrong_password(self):
        login_data = {
            'username': 'ahmad',
            'password': 'wroing password',
        }
        response = self.client.post(reverse_lazy('login'), login_data)
        self.assertEqual(response.status_code, 200)

    def test_login_non_existing_user(self):
        login_data = {
            'username': 'arjang',
            'password': 'password',
        }
        response = self.client.post(reverse_lazy('login'), login_data)
        self.assertEqual(response.status_code, 200)


class SignupViewTest(TestCase):
    def test_page_status(self):
        response = self.client.get(reverse_lazy('register'))
        self.assertEqual(response.status_code, 200)

    def test_valid_new_user_creation(self):
        user_data = {
            'username': 'ahmad',
            'email': 'ahmad@gmail.com',
            'password': 'password',
            'confirm_password': 'password',
            'first_name': 'ahmad',
            'last_name': 'ahmad',
            'id_code': '123456'
        }
        response = self.client.post(reverse_lazy('register'), user_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(SystemUser.objects.filter(id_code=user_data['id_code']).exists())

    def test_invalid_new_user_password_not_equal_to_confirmation(self):
        user_data = {
            'username': 'ahmad',
            'email': 'ahmad@gmail.com',
            'password': 'password',
            'confirm_password': 'wrong_password',
            'first_name': 'ahmad',
            'last_name': 'ahmad',
            'id_code': '123456'
        }
        SystemUser.objects.filter(id_code=user_data['id_code']).delete()
        response = self.client.post(reverse_lazy('register'), user_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(SystemUser.objects.filter(id_code=user_data['id_code']).exists())

    def test_invalid_new_user_username_already_exist(self):
        user_data = {
            'username': 'ahmad',
            'email': 'ahmad@gmail.com',
            'password': 'password',
            'confirm_password': 'password',
            'first_name': 'ahmad',
            'last_name': 'ahmad',
            'id_code': '123456'
        }
        response = self.client.post(reverse_lazy('register'), user_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(SystemUser.objects.filter(id_code=user_data['id_code']).exists())
        response = self.client.post(reverse_lazy('register'), user_data)
        self.assertEqual(response.status_code, 200)