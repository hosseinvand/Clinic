from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy

from reservation.models import SystemUser


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