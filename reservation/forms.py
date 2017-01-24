from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.db.backends.dummy.base import IntegrityError
from django.forms.models import ModelForm, fields_for_model
from reservation import jalali
from reservation.models import SystemUser, Doctor, Office, Reservation


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "نام کاربری"
        self.fields['password'].label = "رمز عبور"
        self.fields['username'].error_messages = {
            'required': 'نام کاربری اجباری است',
            'invalid': 'مقدار ورودی نامعتبر است'
        }
        self.fields['password'].error_messages = {
            'required': 'رمز عبور اجباری است',
            'invalid': 'مقدار ورودی نامعتبر است'
        }
        self.error_messages = {
            'invalid_login': "نام کاربری یا رمز عبور نادرست است!",
            'inactive': "این حساب غیر فعال است!"
        }


class SystemUserRegisterForm(UserCreationForm):

    id_code = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super(SystemUserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].error_messages = {
            'required': 'نام کاربری اجباری است',
            'invalid': 'مقدار ورودی نامعتبر است',
            'unique': 'نام کاربری توسط شخص دیگری ثبت شده‌است',
        }
        self.fields['password1'].error_messages = {
            'required': 'رمز عبور اجباری است',
            'invalid': 'مقدار ورودی نامعتبر است',
        }
        self.fields['password2'].error_messages = {
            'required': 'رمز عبور اجباری است',
            'invalid': 'مقدار ورودی نامعتبر است',
        }
        self.fields['email'].error_messages = {
            'required': 'ایمیل اجباری است',
            'invalid': 'مقدار ورودی نامعتبر است',
        }
        self.error_messages = {
            'password_entirely_numeric': 'رمز عبور نباید کاملا عددی باشد',
            'password_too_short': 'رمز عبور کوتاه است. رمز شما باید حداقل %(min_length)d کاراکتر داشته باشد.',
            'password_mismatch': 'رمز عبور با تکرار آن برابر نیست',
            'invalid_melli_code': 'کد ملی صحیح نیست',
            'id_code_exists': 'کد ملی قبلا ثبت شده است',
        }

    def clean(self):
        cleaned_data = super(SystemUserRegisterForm, self).clean()
        id_code = cleaned_data.get('id_code')
        try:
            if len(id_code) != 10:
                raise ValueError
            id_code = int(id_code)
            if SystemUser.objects.filter(id_code=id_code).exists():
                raise forms.ValidationError(
                    self.error_messages['id_code_exists'],
                    code='id_code_exists',
                )
        except (TypeError, ValueError):
            raise forms.ValidationError(
                self.error_messages['invalid_melli_code'],
                code='invalid_melli_code',
            )
        return cleaned_data

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2


class DoctorRegisterForm(ModelForm):

    class Meta:
        model = Doctor
        fields = '__all__'

        labels = {
            'doctor_code': "شماره نظام پزشکی",
            'education': "میزان تحصیلات",
            'speciality': "تخصص",
            'insurance': "بیمه‌های تحت پوشش",
            'price': "قیمت ویزیت",
            'cv': "رزومه",
            'contract': "آپلود فایل قرارداد...",
        }

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
        error_messages = {
            'opening_days': {
                'required': "شما باید حداقل یک روز هفته را انتخاب کنید."
            },
        }
        labels = {
            'city': "شهر",
            'address': "آدرس",
            'phone': "تلفن",
            'telegram': "کانال تلگرام",
            'from_hour': "از",
            'to_hour': "تا",
            'base_time': "مدت زمان ویزیت هر بیمار(دقیقه)",
            'opening_days': "روزهای کاری",
        }

    def clean(self):
        cleaned_data = super(ClinicForm, self).clean()
        if cleaned_data.get("from_hour") > cleaned_data.get("to_hour"):
            raise forms.ValidationError('ساعت شروع کار باید از ساعت پایان کار کمتر باشد')
        print("opening days:", cleaned_data.get("opening_days"))
        return cleaned_data


class DoctorSearchForm(ModelForm):

    name = forms.CharField(label="نام", widget=forms.TextInput,required=False)
    max_price = forms.IntegerField(label="بیشینه قیمت", widget=forms.NumberInput, required=False)
    city = fields_for_model(Office, labels="شهر")['city']
    from_hour = fields_for_model(Office, labels="از ساعت")['from_hour']
    to_hour = fields_for_model(Office, labels="تا ساعت")['to_hour']
    # days = fields_for_model(Office)['opening_days']

    class Meta:
        model = Doctor
        fields = ['education', 'speciality', 'insurance']

        labels = {
            'education': "تحصیلات",
            'speciality': "تخصص",
            'insurance': "بیمه‌ی تحت پوشش",

        }


class SystemUserUpdateForm(ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    id_code = forms.CharField(max_length=10, min_length=10)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super(SystemUserUpdateForm, self).clean()
        id_code = cleaned_data.get('id_code')
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if (password or confirm_password) and password != confirm_password:
            raise forms.ValidationError(
                "رمز عبور و تکرار رمز عبور مشابه نیست!"
            )
        try:
            int(id_code)
            if SystemUser.objects.filter(id_code=id_code).exclude(user=self.instance).exists():
                raise forms.ValidationError('کد ملی قبلا در سیستم ثبت شده است.')
        except (TypeError, ValueError):
            raise forms.ValidationError(
                "کد ملی را به صورت صحیح وارد نمایید."
            )
        return cleaned_data

    def save(self, commit=True):
        user = super(SystemUserUpdateForm, self).save(commit=False)
        SystemUser.objects.filter(user=user).update(id_code=self.cleaned_data.get('id_code', None))
        password = self.cleaned_data.get('password', None)
        if password:
            user.set_password(password)
        user.save()
        return user

class ReservationDateTimeForm(ModelForm):

    doctor_pk = forms.IntegerField()
    patient_pk = forms.IntegerField()
    date = forms.CharField()
    # from_time = forms.TimeField(widget=SelectTimeWidget(minute_step=15, second_step=30, twelve_hr=True))
    # to_time = forms.TimeField(widget=SelectTimeWidget(minute_step=15, second_step=30, twelve_hr=True))

    class Meta:
        model = Reservation
        fields = ['from_time', 'to_time']

    def save(self, commit=True):
        time = super(ReservationDateTimeForm, self).save(commit=False)
        time.patient = SystemUser.objects.get(pk=self.cleaned_data.get("patient_pk"))
        print("user patient: ", time.patient)
        time.doctor = Doctor.objects.get(pk=self.cleaned_data.get("doctor_pk"))
        time.date = jalali.Persian(self.cleaned_data.get("date")).gregorian_datetime()
        time.save()
        return time

    def clean(self):
        cleaned_data = super(ReservationDateTimeForm, self).clean()
        if cleaned_data.get("from_time") > cleaned_data.get("to_time"):
            raise forms.ValidationError('زمان آغازی بازه باید از ازمان پایانی آن کمتر باشد.')
        doctor = Doctor.objects.get(pk=self.cleaned_data.get("doctor_pk"))
        if cleaned_data.get("from_time") > doctor.office.to_hour or cleaned_data.get("to_time") < doctor.office.from_hour:
            raise forms.ValidationError('زمان انتخابی شما در بازه‌ی ساعات کاری پزشک نیست')
        return cleaned_data
