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

    def save(self, commit=True):
        username = self.cleaned_data.get('username', None)
        email = self.cleaned_data.get('email', None)
        password = self.cleaned_data.get('password', None)
        first_name = self.cleaned_data.get('first_name', None)
        last_name = self.cleaned_data.get('last_name', None)

        tmp_user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        return Patient.objects.create(user=tmp_user)



class LoginForm(ModelForm):
    username = fields_for_model(User)['username']
    password = fields_for_model(User)['password']

    class Meta:
        model = Patient
        fields = []
