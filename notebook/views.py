import json
from time import sleep

from django.contrib.auth import authenticate, login
from django.core import serializers
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from django.views.generic import TemplateView

from reservation.models import Doctor, Reservation


class MainPageView(TemplateView):
    template_name = 'react_home.html'


class Login(View):

    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        username, password = body['username'], body['password']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        if user:
            login(self.request, user)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=401)


class ReservationsView(View):

    def reservation_to_dict(self, reservation, status):
        return {
            'pk': reservation.id,
            'doctor_pk': reservation.doctor.id,
            'speciality': reservation.doctor.get_speciality_display(),
            'date': reservation.get_jalali,
            'full_name': reservation.doctor.full_name,
            'from': reservation.from_time,
            'to': reservation.to_time,
            'status': status
        }

    def get(self, request, *args, **kwargs):
        reservations = self.request.user.system_user.get_reserve_times()
        data = [self.reservation_to_dict(reservation, reservation.status) for reservation in reservations]
        return JsonResponse(data=data, safe=False)

class DoctorsView(View):

    def get(self, request, *args, **kwargs):
        doctors = Doctor.objects.all()
        data = [{
            'id': doctor.id,
            'education': doctor.get_education_display(),
            'speciality': doctor.get_speciality_display(),
            'city': doctor.city,
            'full_name': doctor.full_name,
            'insuarance': doctor.get_insurance_display(),
            'cv': doctor.cv,
            'price': doctor.price,
            'office': ({
                'city': doctor.city,
                'address': doctor.office.address,
                'from_hour': doctor.office.from_hour,
                'to_hour': doctor.office.to_hour,
                'openning_days': doctor.office.get_opening_days_display(),
                'phone': doctor.office.phone,
                'telegram': doctor.office.telegram
            } if doctor.office else None)
                } for doctor in doctors]
        return JsonResponse(data=data, safe=False)


class DoctorDetailView(View):

    def get(self, request, *args, **kwargs):
        doctor = Doctor.objects.filter(id=kwargs['pk']).first()
        print(doctor.full_name)
        print(doctor.office)
        data = {
            'id': doctor.id,
            'education': doctor.get_education_display(),
            'speciality': doctor.get_speciality_display(),
            'city': doctor.city,
            'full_name': doctor.full_name,
            'insurance': doctor.get_insurance_display(),
            'cv': doctor.cv,
            'price': doctor.price,
            'office': ({
                'city': doctor.city,
                'address': doctor.office.address,
                'from_hour': doctor.office.from_hour,
                'to_hour': doctor.office.to_hour,
                'opening_days': doctor.office.get_opening_days_display(),
                'phone': doctor.office.phone,
                'telegram': doctor.office.telegram
            } if doctor.office else None)
        }
        return JsonResponse(data=data, safe=False)