from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms import forms
from django.test import TestCase
from django.urls import reverse_lazy
import os

from reservation.models import SystemUser, Doctor


class SystemUserTest(TestCase):
    user_data = {
        'username': 'ahmad',
        'email': 'ahmad@gmail.com',
        'password': 'password',
        'confirm_password': 'password',
        'first_name': 'ahmad',
        'last_name': 'ahmad',
        'id_code': '1234567890'
    }

    user_data2 = {
        'username': 'salam',
        'email': 'salam@gmail.com',
        'password': 'test',
        'confirm_password': 'test',
        'first_name': 'salam',
        'last_name': 'iran',
        'id_code': '1111111111'
    }

    def create_system_user(self, data=user_data):
        user_count = User.objects.all().count()
        system_user_count = SystemUser.objects.all().count()
        response = self.client.post(reverse_lazy('register'), data)
        user = User.objects.filter(username=data['username'])
        self.assertTrue(user.exists())
        self.assertTrue(SystemUser.objects.filter(user=user[0]).exists())
        self.assertTrue(SystemUser.objects.filter(id_code=data['id_code']).exists())
        self.assertEqual(User.objects.all().count(), user_count + 1, "db doesn't changed")
        self.assertEqual(SystemUser.objects.all().count(), system_user_count + 1, "db doesn't changed")
        return response

    def test_redirect_to_login(self):
        response = self.client.get(reverse_lazy('systemUserProfile'), follow=True)
        self.assertRedirects(response, '/login/?next=/panel/profile/', 302, 200)

    def test_user_creation(self):
        self.create_system_user()


class DoctorTest(SystemUserTest):
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
        super(DoctorTest, self).setUp()
        upload_file = open(os.path.join(os.path.dirname(__file__), 'test_utils.py'), 'rb')
        self.doctor_data['contract'] = SimpleUploadedFile(upload_file.name, upload_file.read())

    def create_doctor(self, data=doctor_data):
        self.create_system_user()
        doctor_count = Doctor.objects.all().count()
        response = self.client.post(reverse_lazy('doctorRegister'), data)
        doctor = Doctor.objects.filter(doctor_code=self.doctor_data['doctor_code'])
        self.assertEqual(response.status_code, 302)
        self.assertTrue(doctor.exists())
        self.assertTrue(Doctor.objects.filter(education=self.doctor_data['education']).exists())
        self.assertTrue(SystemUser.objects.filter(role=doctor[0]).exists())
        self.assertEqual(Doctor.objects.all().count(), doctor_count + 1, "db doesn't changed")
        return response


class EditSystemUserTest(SystemUserTest):

    def test_user_access(self):
        self.create_system_user()
        response = self.client.get(reverse_lazy('systemUserProfile'))
        self.assertEqual(response.status_code, 200)
        return response

    def test_response_contains_data(self):

        def check_field_initial_value(form, field, value=None):
            self.assertTrue(field in form.initial)
            if value:
                self.assertEqual(form.initial[field], value)
            else:
                self.assertEqual(form.initial[field], self.user_data[field])

        response = self.test_user_access()
        form = response.context['form']
        check_field_initial_value(form, 'username')
        check_field_initial_value(form, 'first_name')
        check_field_initial_value(form, 'last_name')
        check_field_initial_value(form, 'email')
        check_field_initial_value(form, 'id_code')
        self.assertIsNone(form['password'].value())
        self.assertIsNone(form['confirm_password'].value())

    def test_invalid_id_code(self):
        self.test_user_access()
        new_data = self.user_data.copy()
        new_data['id_code'] = '1234'
        response = self.client.post(reverse_lazy('systemUserProfile'), new_data)
        self.assertFormError(response, 'form', 'id_code', 'Ensure this value has at least 10 characters (it has %d).'
                             % len(new_data['id_code']))

    def test_duplicate_id_code(self):
        self.test_user_access()
        new_data = self.user_data2.copy()
        self.create_system_user(data=new_data)
        new_data['id_code'] = self.user_data['id_code']
        response = self.client.post(reverse_lazy('systemUserProfile'), new_data)
        self.assertEqual(response.status_code, 200)
        self.assertRaises(forms.ValidationError, response.context['form'].clean)

    def test_duplicate_username(self):
        self.test_user_access()
        new_data = self.user_data2.copy()
        self.create_system_user(data=new_data)
        new_data['username'] = self.user_data['username']
        response = self.client.post(reverse_lazy('systemUserProfile'), new_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')

    def test_valid_submit(self):
        self.test_user_access()
        response = self.client.post(reverse_lazy('systemUserProfile'), self.user_data2)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user_data2['id_code'], User.objects.filter(username=self.user_data2['username'])[0].system_user.id_code)

    def test_valid_id_code_submit(self):
        self.test_user_access()
        new_data = self.user_data.copy()
        new_data['id_code'] = self.user_data2['id_code']
        response = self.client.post(reverse_lazy('systemUserProfile'), new_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user_data2['id_code'], User.objects.filter(username=self.user_data['username'])[0].system_user.id_code)

    def test_passwords_did_not_match(self):
        self.test_user_access()
        new_data = self.user_data.copy()
        new_data['confirm_password'] = 'wrong'
        response = self.client.post(reverse_lazy('systemUserProfile'), new_data)
        self.assertEqual(response.status_code, 200)
        self.assertRaises(forms.ValidationError, response.context['form'].clean)

    def test_change_password(self):
        self.test_user_access()
        new_data = self.user_data.copy()
        new_password = 'new_password'
        new_data['password'] = new_password
        new_data['confirm_password'] = new_password
        response = self.client.post(reverse_lazy('systemUserProfile'), new_data)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse_lazy('login'), {'username': new_data['username'],
                                                            'password': new_password})
        self.assertEqual(response.status_code, 302)

