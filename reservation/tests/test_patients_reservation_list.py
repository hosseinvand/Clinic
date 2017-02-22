import datetime

from django.test import TestCase
from django.urls import reverse_lazy

from media.contracts.test_utils import create_multiple_doctors
from reservation import models


class ShowReserveListTest(TestCase):
    def test_today_list(self):
        create_multiple_doctors(5)

        doctor = models.Doctor.objects.first()
        self.client.login(username='doctor0', password='password0')
        for i, user in enumerate(models.SystemUser.objects.all()):
            reserve = models.Reservation.objects.create(from_time=doctor.office.from_hour,
                                                        to_time=doctor.office.to_hour,
                                                        date=datetime.date.today(),
                                                        patient=user, doctor=doctor)
            range_nums = reserve.get_available_times()
            reserve.range_num = range_nums[0]['range_num']
            reserve.save()
        response = self.client.get(reverse_lazy('reservationList'))
        reservation_list = response.context_data['reservation_list']
        self.assertEqual(len(reservation_list), 5)
        for reservation in reservation_list:
            self.assertEqual(reservation.date, datetime.date.today())
        self.assertEqual(response.status_code, 200)

    def test_yesterday_list(self):
        create_multiple_doctors(5)

        doctor = models.Doctor.objects.first()
        self.client.login(username='doctor0', password='password0')
        for i, user in enumerate(models.SystemUser.objects.all()):
            reserve = models.Reservation.objects.create(from_time=doctor.office.from_hour,
                                                        to_time=doctor.office.to_hour,
                                                        date=datetime.date.today() - datetime.timedelta(1),
                                                        patient=user, doctor=doctor)
            range_nums = reserve.get_available_times()
            reserve.range_num = range_nums[0]['range_num']
            reserve.save()
        response = self.client.get(reverse_lazy('reservationList'))
        self.assertEqual(response.status_code, 200)
        data = response.context_data
        self.assertEqual(len(data['reservation_list']), 0)

    def test_this_week_list(self):
        create_multiple_doctors(5)

        doctor = models.Doctor.objects.first()
        self.client.login(username='doctor0', password='password0')
        saturday = datetime.datetime.strptime('18022017', '%d%m%Y').date()
        for i, user in enumerate(models.SystemUser.objects.all()):
            reserve = models.Reservation.objects.create(from_time=doctor.office.from_hour,
                                                        to_time=doctor.office.to_hour,
                                                        date=saturday + datetime.timedelta(2 * i),
                                                        patient=user, doctor=doctor)
            range_nums = reserve.get_available_times()
            reserve.range_num = range_nums[0]['range_num']
            reserve.save()
        response = self.client.get('{}{}'.format(reverse_lazy('reservationList'), '?week=on'))
        self.assertEqual(response.status_code, 200)
        data = response.context_data
        self.assertEqual(len(data['reservation_list']), 4)

        response = self.client.get('{}{}'.format(reverse_lazy('reservationList'), '?day=1395-12-07&week=on'))
        self.assertEqual(response.status_code, 200)
        data = response.context_data
        self.assertEqual(len(data['reservation_list']), 1)

        response = self.client.get('{}{}'.format(reverse_lazy('reservationList'), '?day=1395-12-08'))
        self.assertEqual(response.status_code, 200)
        data = response.context_data
        self.assertEqual(len(data['reservation_list']), 1)
