from django.contrib.auth.models import User
from django.forms import forms
from django.test import TestCase
from django.urls import reverse_lazy

from reservation.models import SystemUser, Secretary, DOCTOR_ROLE_ID, SECRETARY_ROLE_ID, Patient, PATIENT_ROLE_ID
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
            role = Patient()
            role.save()
            SystemUser.objects.create(user=tmp_user, id_code=data['id_code'])
            SystemUser.objects.filter(user=tmp_user).update(role=role)
        user = User.objects.filter(username=data['username'])
        self.assertTrue(user.exists())
        self.assertTrue(SystemUser.objects.filter(user=user[0]).exists())
        self.assertTrue(SystemUser.objects.filter(id_code=data['id_code']).exists())
        self.assertEqual(User.objects.all().count(), user_count + 1, "db doesn't changed")
        self.assertEqual(SystemUser.objects.all().count(), system_user_count + 1, "db doesn't changed")
        return SystemUser.objects.get(user=user)

    def add_secretary_and_add_non_valid_secretary(self):
        candidate_system_user = self.create_system_user(data=self.user_data, should_login=False)
        doctor_system_user = create_multiple_doctors(1)[0]
        self.client.login(username="doctor0", password="password0")
        self.assertEqual(doctor_system_user.role.get_role_id(), DOCTOR_ROLE_ID)

        response = self.client.get(reverse_lazy('ManageSecretary'))
        self.assertEqual(response.status_code, 200)

        # add valid secretary
        secretary_count_before = len(Secretary.objects.filter(office=doctor_system_user.role.office))
        response = self.client.post(reverse_lazy('ManageSecretary'), {'username': candidate_system_user.user.username})
        secretary_count_after = len(Secretary.objects.filter(office=doctor_system_user.role.office))
        self.assertEqual(response.status_code, 302)
        # candidate_system_user = SystemUser.objects.get(id_code=self.user_data['id_code'])
        candidate_system_user.refresh_from_db()
        self.assertEqual(candidate_system_user.role.get_role_id(), SECRETARY_ROLE_ID)
        self.assertEqual(candidate_system_user.role.office, doctor_system_user.role.office)
        self.assertEqual(secretary_count_before + 1, secretary_count_after)

        # add non valid secretary
        secretary_count_before = len(Secretary.objects.filter(office=doctor_system_user.role.office))
        response = self.client.post(reverse_lazy('ManageSecretary'), {'username': 'fake_username'})
        secretary_count_after = len(Secretary.objects.filter(office=doctor_system_user.role.office))
        self.assertEqual(secretary_count_before, secretary_count_after)

        # remove secretary
        secretary_count_before = len(Secretary.objects.filter(office=doctor_system_user.role.office))
        response = self.client.post(reverse_lazy('deleteSecretary'), {'username': candidate_system_user.user.username})
        secretary_count_after = len(Secretary.objects.filter(office=doctor_system_user.role.office))
        self.assertEqual(secretary_count_before - 1, secretary_count_after)