from django.contrib.auth.models import User
from django.forms.models import ModelForm, fields_for_model
from reservation.models import Patient

__author__ = 'mahshid'


class PatientRegisterForm(ModelForm):
    username = fields_for_model(User)['username']
    email = fields_for_model(User)['email']
    password = fields_for_model(User)['password']
    first_name = fields_for_model(User)['first_name']
    last_name = fields_for_model(User)['last_name']

    class Meta:
        model = Patient
        fields = []