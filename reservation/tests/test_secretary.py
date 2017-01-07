from django.contrib.auth.models import User
from django.forms import forms
from django.test import TestCase
from django.urls import reverse_lazy

from reservation.models import SystemUser, Secretary, DOCTOR_ROLE_ID, SECRETARY_ROLE_ID
from reservation.tests.test_utils import create_office, create_multiple_doctors, create_test_user


class SecretaryTest(TestCase):
    user_data = {
        'username': 'ahmad',
        'email': 'ahmad@gmail.com',
        'password': 'password',
        'confirm_password': 'password',
        'first_name': 'ahmad',
        'last_name': 'ahmad',
        'id_code': '0034567890'
    }

    office_data = {
        'phone': '02144223355',
        'city': 'Tehran',
        'from_hour': '4',
        'to_hour': '8'
    }

    user_data2 = {
        'username': 'salam',
        'email': 'salam@gmail.com',
        'password': 'test',
        'confirm_password': 'test',
        'first_name': 'salam',
        'last_name': 'iran',
        'id_code': '0011111111'
    }

    def create_system_user(self, data=user_data, should_login=False):
        user_count = User.objects.all().count()
        system_user_count = SystemUser.objects.all().count()
        if should_login:
            self.client.post(reverse_lazy('register'), data)
        else:
            tmp_user = create_test_user(**data)
            SystemUser.objects.create(user=tmp_user, id_code=data['id_code'])
        user = User.objects.filter(username=data['username'])
        self.assertTrue(user.exists())
        self.assertTrue(SystemUser.objects.filter(user=user[0]).exists())
        self.assertTrue(SystemUser.objects.filter(id_code=data['id_code']).exists())
        self.assertEqual(User.objects.all().count(), user_count + 1, "db doesn't changed")
        self.assertEqual(SystemUser.objects.all().count(), system_user_count + 1, "db doesn't changed")
        return SystemUser.objects.get(user=user)


    # def create_secretary(self, user_data=user_data, office_data = office_data, should_login=False):
    #     system_user = self.create_system_user(data=user_data, should_login=should_login)
    #     office = create_office(self, **office_data)
    #     secretary = Secretary.objects.create(office=office)
    #     system_user.role = secretary
    #     system_user.save()
    #     return secretary

    def add_secretary(self):
        candidate_system_user = self.create_system_user(data=self.user_data, should_login=False)
        doctor_system_user = create_multiple_doctors(1)[0]
        self.client.login(username="doctor0", password="password0")
        self.assertEqual(doctor_system_user.role.get_role_id(), DOCTOR_ROLE_ID)

        response = self.client.get(reverse_lazy('ManageSecretary'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse_lazy('ManageSecretary'), {'username': candidate_system_user.user.username})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(candidate_system_user.role.get_role_id(), SECRETARY_ROLE_ID) # can i use this sysuser object?
        self.assertEqual(candidate_system_user.role.office, doctor_system_user.role.office)


    def test_adding_secertary(self):
        pass

    def test_redirect_to_login(self):
        response = self.client.get(reverse_lazy('systemUserProfile'), follow=True)
        self.assertRedirects(response, '/login/?next=/panel/profile/', 302, 200)

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

