from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy

from reservation.models import SystemUser, Secretary, DOCTOR_ROLE_ID, SECRETARY_ROLE_ID, Patient, PATIENT_ROLE_ID, \
    Reservation
from reservation.tests.test_utils import create_multiple_doctors, create_test_user


class EditOfficeTest(TestCase):
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

    def test_edit_office(self):
        doctor = create_multiple_doctors(1)[0].role
        self.client.login(username="doctor0", password="password0")

        new_office_data = {
            'city': 'Yazd',
            'address': 'address',
            'phone': '02122334411',
            'telegram': 'telegram',
            'from_hour': 9,
            'to_hour': 13,
            'base_time': 15,
            'opening_days': ['sat']
        }

        response = self.client.post(reverse_lazy('updateClinic',), new_office_data)
        self.assertEqual(response.status_code, 302)
        office = doctor.office
        office.refresh_from_db()

        self.assertEqual(office.city, new_office_data['city'])
        self.assertEqual(office.address, new_office_data['address'])
        self.assertEqual(office.phone, new_office_data['phone'])
        self.assertEqual(office.from_hour, new_office_data['from_hour'])
        self.assertEqual(office.to_hour, new_office_data['to_hour'])
        self.assertEqual(office.base_time, new_office_data['base_time'])
        self.assertEqual(office.opening_days, new_office_data['opening_days'])

        new_office_data['from_hour'] = 15
        response = self.client.post(reverse_lazy('updateClinic', ), new_office_data)
        self.assertEqual(response.status_code, 200)