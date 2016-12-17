from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms.models import ModelForm, fields_for_model
from reservation.models import Patient


class PatientRegisterForm(ModelForm):
    username = fields_for_model(User)['username']
    # email = fields_for_model(User)['email']
    email = forms.EmailField(widget=forms.EmailInput())
    # password = fields_for_model(User)['password']
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    first_name = fields_for_model(User)['first_name']
    last_name = fields_for_model(User)['last_name']

    class Meta:
        model = Patient
        fields = []

    def clean_username(self):
        cleaned_data = super(PatientRegisterForm, self).clean()
        if User.objects.filter(username=cleaned_data.get("username")).exists():
            raise forms.ValidationError('Username already exists!')
        return cleaned_data.get("username")

    def clean(self):
        cleaned_data = super(PatientRegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match!"
            )
        return cleaned_data

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
    # password = fields_for_model(User)['password']
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Patient
        fields = []

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        try:
            User.objects.get(username=cleaned_data.get("username"))
        except User.DoesNotExist:
            raise forms.ValidationError('Username "%s" Does not exist.' % cleaned_data.get("username"))
        return cleaned_data

    def clean_password(self):
        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')
        if not password or len(password) < 1:
            raise forms.ValidationError("Please enter your password")

        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Your password is wrong!")
        return password
