from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy

from reservation.models import SystemUser, Patient, Reservation
from reservation.tests.utils import create_multiple_doctors, create_test_user


class ReservationTest(TestCase):
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

    def test_request_reservation(self):
        patient = self.create_system_user(data=self.user_data, should_login=False)
        doctor = create_multiple_doctors(1)[0].role
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])

        reservation_count_before = len(Reservation.objects.all())
        date = doctor.office.get_available_days()[0][0]
        response = self.client.post(reverse_lazy('reservation', kwargs={'pk': doctor.pk}), {
            'from_time': '8',
            'to_time': '10',
            'date': str(date),
            'patient_pk': patient.pk,
            'doctor_pk': doctor.pk,
        })
        reservation_count_after = len(Reservation.objects.all())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(reservation_count_before + 1, reservation_count_after)
        self.assertTrue(Reservation.objects.filter(patient=patient, doctor=doctor).exists())

    def test_request_invalid_reservation(self):
        patient = self.create_system_user(data=self.user_data, should_login=False)
        doctor = create_multiple_doctors(1)[0].role
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])

        reservation_count_before = len(Reservation.objects.all())
        date = doctor.office.get_available_days()[0][0]
        response = self.client.post(reverse_lazy('reservation', kwargs={'pk': doctor.pk}), {
            'from_time': '16',
            'to_time': '12',
            'date': str(date),
            'patient': patient.pk,
            'doctor': doctor.pk,
        })
        reservation_count_after = len(Reservation.objects.all())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(reservation_count_before, reservation_count_after)
