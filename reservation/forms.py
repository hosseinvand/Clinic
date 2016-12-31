from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms.models import ModelForm, fields_for_model
from reservation.models import SystemUser, Doctor, Office


class SystemUserRegisterForm(ModelForm):
    username = fields_for_model(User)['username']
    # email = fields_for_model(User)['email']
    email = forms.EmailField(widget=forms.EmailInput())
    # password = fields_for_model(User)['password']
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    first_name = fields_for_model(User)['first_name']
    last_name = fields_for_model(User)['last_name']

    class Meta:
        model = SystemUser
        fields = ['id_code']

    #TODO: moved to clean method...
    # def clean_username(self):
    #     # print("clean_username entrance")
    #     cleaned_data = super(SystemUserRegisterForm, self).clean()
    #     if User.objects.filter(username=cleaned_data.get("username")).exists():
    #         raise forms.ValidationError('Username already exists!')
    #     return cleaned_data.get("username")

    def clean(self):
        cleaned_data = super(SystemUserRegisterForm, self).clean()
        if User.objects.filter(username=cleaned_data.get("username")).exists():
            raise forms.ValidationError('نام کاربری وارد شده پیش از این توسط شخص دیگری ثبت شده‌است!')
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(
                "رمز عبور و تکرار رمز عبور مشابه نیست!"
            )
        return cleaned_data

    def save(self, commit=True):
        username = self.cleaned_data.get('username', None)
        email = self.cleaned_data.get('email', None)
        password = self.cleaned_data.get('password', None)
        first_name = self.cleaned_data.get('first_name', None)
        last_name = self.cleaned_data.get('last_name', None)
        id_code = self.cleaned_data.get('id_code', None)

        tmp_user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        return SystemUser.objects.create(user=tmp_user, id_code=id_code)


class LoginForm(ModelForm):
    username = fields_for_model(User)['username']
    # password = fields_for_model(User)['password']
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = SystemUser
        fields = []

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        try:
            User.objects.get(username=cleaned_data.get("username"))
        except User.DoesNotExist:
            raise forms.ValidationError('Username "%s" Does not exist.' % cleaned_data.get("username"))

        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')
        if not password or len(password) < 1:
            raise forms.ValidationError("لطفا رمز عبور خود را وارد نمایید")

        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("رمز عبور شما نادرست است!")
        return cleaned_data


class DoctorRegisterForm(ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'

    def clean(self):
        cleaned_data = super(DoctorRegisterForm, self).clean()
        if Doctor.objects.filter(doctor_code=cleaned_data.get("doctor_code")).exists():
            raise forms.ValidationError('شماره نظام پزشکی قبلا در سیستم ثبت شده است.')
        if not cleaned_data.get("contract"):
            raise forms.ValidationError('فرم قرارداد امضا شده را آپلود نمایید.')
        return cleaned_data

class ClinicForm(ModelForm):

    class Meta:
        model = Office
        fields = '__all__'

    def clean(self):
        cleaned_data = super(ClinicForm, self).clean()
        if Office.objects.filter(phone=cleaned_data.get("phone")).exists():
            raise forms.ValidationError('این شماره تلفن برای مطب شخص دیگری ثبت شده‌است!')
        if cleaned_data.get("from_hour") > cleaned_data.get("to_hour"):
            raise forms.ValidationError('ساعت شروع کار باید از ساعت پایان کار کمتر باشد')
        print("opening days:", cleaned_data.get("opening_days"))
        return cleaned_data