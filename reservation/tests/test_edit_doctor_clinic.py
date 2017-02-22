from django.urls import reverse_lazy

from reservation.models import CITY_NAMES, HOURS, BASE_TIMES, WEEK_DAYS
from reservation.tests.test_edit_system_user import DoctorTest


class EditDoctorClinicTest(DoctorTest):
    clinic_data = {
        'city': CITY_NAMES[0],
        'address': 'Azadi street',
        'phone': '021-52627282',
        'telegram': '@doctor',
        'from_hour': HOURS[8][0],
        'to_hour': HOURS[16][0],
        'base_time': BASE_TIMES[2][0],
        'opening_days': [WEEK_DAYS[2][0], WEEK_DAYS[3][0]],
    }

    def test_redirect_to_login(self):
        response = self.client.get(reverse_lazy('updateClinic'), follow=True)
        self.assertRedirects(response, '/login/?next=/panel/clinic/edit', 302, 200)

    def test_redirect_to_panel(self):
        self.create_system_user()
        response = self.client.get(reverse_lazy('updateClinic'), follow=True)
        self.assertRedirects(response, reverse_lazy('panel'), 302, 200)
