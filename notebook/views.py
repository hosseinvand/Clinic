import json

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

from reservation.models import Doctor


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


class DoctorsView(View):

    def get(self, request, *args, **kwargs):
        doctors = Doctor.objects.all()
        data = [{
            'id': doctor.id,
            'education': doctor.get_education_display(),
            'speciality': doctor.get_speciality_display(),
            'city': doctor.city,
            'full_name': doctor.full_name
                } for doctor in doctors]
        return JsonResponse(data=data, safe=False)