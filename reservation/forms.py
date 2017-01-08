from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.gis.admin import widgets
from django.db.utils import IntegrityError
from django.forms.models import ModelForm, fields_for_model
from reservation import jalali
from reservation.models import SystemUser, Doctor, Office, Reservation, RESERVATION_STATUS


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

    name = forms.CharField(widget=forms.TextInput,required=False)
    max_price = forms.IntegerField(widget=forms.NumberInput, required=False)
    city = fields_for_model(Office)['city']
    from_hour = fields_for_model(Office)['from_hour']
    to_hour = fields_for_model(Office)['to_hour']
    # days = fields_for_model(Office)['opening_days']

    class Meta:
        model = Doctor
        fields = ['education', 'speciality', 'insurance']


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
        time.status = RESERVATION_STATUS[0][0]
        time.save()
        return time

    def clean(self):
        cleaned_data = super(ReservationDateTimeForm, self).clean()
        if cleaned_data.get("from_time") > cleaned_data.get("to_time"):
            print("خاک تو سرت!")
            raise forms.ValidationError('زمان آغازی بازه باید از ازمان پایانی آن کمتر باشد.')
        doctor = Doctor.objects.get(pk=self.cleaned_data.get("doctor_pk"))
        if cleaned_data.get("from_time") > doctor.office.to_hour or cleaned_data.get("to_time") < doctor.office.from_hour:
            raise forms.ValidationError('زمان انتخابی شما در بازه‌ی ساعات کاری پزشک نیست')
        return cleaned_data
