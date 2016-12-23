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

    def test_page_status_for_non_doctor_user(self):
        tmp_user = create_test_user(username='ahmad', password='password')
        SystemUser.objects.create(user=tmp_user, id_code='123456', role=None)
        self.client.logout()
        self.client.login(username='ahmad', password='password')
        response = self.client.get(reverse_lazy('addClinic'))
        self.assertNotEqual(response.status_code, 200)

    def test_add_new_offic(self):
        office_data = {
            'city': 'Zanjan',
            'address': 'میدان انقلاب',
            'phone': '0223344213',
            'telegram': 'ahmadClinic',
        }
        user = create_test_doctor('123456', 'ahmad', 'password')
        self.client.logout()
        self.client.login(username='ahmad', password='password')
        response = self.client.post(reverse_lazy('addClinic'), office_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(user.role.offices.all().filter(address=office_data['address'], phone=office_data['phone']).exists())


class DoctorSignupViewTest(TestCase):
    def test_page_status_for_anonymous_user(self):
        self.client.logout()
        response = self.client.get(reverse_lazy('doctorRegister'))
        self.assertNotEqual(response.status_code, 200)

    def test_page_status_for_non_doctor_user(self):
        tmp_user = create_test_user(username='ahmad', password='password')
        SystemUser.objects.create(user=tmp_user, id_code='123456', role=None)
        self.client.logout()
        self.client.login(username='ahmad', password='password')
        response = self.client.get(reverse_lazy('doctorRegister'))
        self.assertNotEqual(response.status_code, 200)

    def test_valid_new_doctor_creation(self):
        doctor_data = {
            'doctor_code': '123456',
            'education': 'S',
            'speciality': 'Eye',
            'insurance': 'Iran',
            'price': 35000,
            'cv': 'maybe not the best doc in the world but the happiest one :)'
        }
        response = self.client.post(reverse_lazy('doctorRegister'), doctor_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Doctor.objects.filter(doctor_code=doctor_data['doctor_code']).exists())

    def test_invalid_new_doctor_code_already_exist(self):
        doctor_data = {
            'doctor_code': '123456',
            'education': 'S',
            'speciality': 'Eye',
            'insurance': 'Iran',
            'price': 35000,
            'cv': 'maybe not the best doc in the world but the happiest one :)'
        }
        response = self.client.post(reverse_lazy('doctorRegister'), doctor_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Doctor.objects.filter(doctor_code=doctor_data['doctor_code']).exists())
        response = self.client.post(reverse_lazy('doctorRegister'), doctor_data)
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