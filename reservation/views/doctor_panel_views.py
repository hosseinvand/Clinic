import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls.base import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.views.generic.base import View
from django.views.generic.list import ListView

from reservation.forms import *
from reservation.mixins import PatientRequiredMixin, DoctorRequiredMixin, DoctorSecretaryRequiredMixin
from reservation.models import Secretary, Patient, PATIENT_ROLE_ID


class DoctorCreateView(LoginRequiredMixin, PatientRequiredMixin, CreateView):
    model = Doctor
    template_name = 'doctor_register.html'
    success_url = reverse_lazy('mainPage')
    form_class = DoctorRegisterForm

    def form_valid(self, form):
        response = super(DoctorCreateView, self).form_valid(form)
        doctor = Doctor.objects.get(doctor_code=form.cleaned_data['doctor_code'])
        SystemUser.objects.filter(user=self.request.user).update(role=doctor)
        return response


class ManageSecretary(LoginRequiredMixin, ListView):
    selected = "manageSecretary"
    model = Secretary
    template_name = 'panel.html'

    def get_queryset(self):
        object_list = self.model.objects.filter(office=self.request.user.system_user.role.office)
        return object_list

    @staticmethod
    def get_system_user_by_username(username):
        """
        :param username
        :return: system user that has username = username
        """
        try:
            return User.objects.get(username=username).system_user
        except User.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        secretary_username = request.POST.get('username')
        secretary_user = self.get_system_user_by_username(secretary_username)

        if not secretary_user:
            return HttpResponse("خطا! منشی وجود ندارد.")

        if self.entered_username_can_become_secretary(secretary_user):
            office = request.user.system_user.role.office
            secretary_role = Secretary(office=office)
            secretary_role.save()
            secretary_user.role = secretary_role
            secretary_user.save()
        return redirect(reverse_lazy("ManageSecretary"))

    @staticmethod
    def entered_username_can_become_secretary(secretary_user):
        """
        :param secretary_user:
        :return: check whether a user role is patient (can become secretary) or not
        """
        return secretary_user.role.get_role_id() == PATIENT_ROLE_ID


class DeleteSecretary(LoginRequiredMixin, DoctorRequiredMixin, View):

    @staticmethod
    def post(request):
        username = request.POST.get('username', None)
        user = User.objects.get(username=username).system_user
        last_user_role = user.role
        patient_role = Patient()
        patient_role.save()
        user.role = patient_role
        user.save()
        last_user_role.delete()
        return JsonResponse({})


class ReserveTime(LoginRequiredMixin, DoctorSecretaryRequiredMixin, View):

    @staticmethod
    def post(request):
        reservation_pk = request.POST.get('reservationPk', None)
        range_num = request.POST.get('rangeNum', None)
        Reservation.objects.filter(pk=reservation_pk).update(range_num=range_num)
        return JsonResponse({})


class RejectRequestedTime(LoginRequiredMixin, DoctorSecretaryRequiredMixin, View):

    @staticmethod
    def post(request):
        reservation_pk = request.POST.get('reservationPk', None)
        Reservation.objects.filter(pk=reservation_pk).update(rejected=True)
        return JsonResponse({})


class AddClinicView(LoginRequiredMixin, DoctorRequiredMixin, CreateView):
    selected = "addClinic"
    model = Office
    template_name = 'panel.html'
    success_url = reverse_lazy('panel')
    form_class = ClinicForm

    def form_valid(self, form):
        response = super(AddClinicView, self).form_valid(form)
        office = Office.objects.filter(address=form.cleaned_data['address'], phone=form.cleaned_data['phone'])[0]
        doctor = SystemUser.objects.get(user=self.request.user).role
        doctor.office = office
        doctor.save()
        return response


class UpdateClinicView(LoginRequiredMixin, DoctorSecretaryRequiredMixin, UpdateView):
    selected = "updateClinic"
    model = Office
    template_name = 'panel.html'
    success_url = reverse_lazy('panel')
    form_class = ClinicForm

    def get_object(self, queryset=None):
        x = SystemUser.objects.get(user=self.request.user).role.office
        return x


class ManageReservations(LoginRequiredMixin, DoctorSecretaryRequiredMixin, ListView):
    selected = "reservation"
    template_name = 'panel.html'

    def get_queryset(self):
        return self.request.user.system_user.role.get_available_reservation_requests()


class SecretaryPanel(LoginRequiredMixin, ListView):
    selected = "panel"
    template_name = 'panel.html'
    context_object_name = 'accepted'

    def get_queryset(self):
        return self.request.user.system_user.get_accepted_reserve_times()

    def get_context_data(self, **kwargs):
        context = super(SecretaryPanel, self).get_context_data(**kwargs)
        context['pending'] = self.request.user.system_user.get_pending_reserve_times()
        context['rejected'] = self.request.user.system_user.get_rejected_reserve_times()
        context['expired'] = self.request.user.system_user.get_expired_reserve_times()
        return context


class ReservationListPanel(LoginRequiredMixin, DoctorSecretaryRequiredMixin, ListView):
    selected = "reservationList"
    template_name = 'panel.html'

    def get_context_data(self, **kwargs):
        context = super(ReservationListPanel, self).get_context_data(**kwargs)
        context['day'] = self.request.GET.get("day", "")
        if not context['day']:
            context['day'] = jalali.Gregorian(datetime.date.today()).persian_string(
                date_format="{}-{}-{}")
        context['week'] = self.request.GET.get("week", "")
        return context

    def get_queryset(self):
        week = self.request.GET.get("week")
        day = self.request.GET.get("day", "")
        date = datetime.date.today()
        try:
            date = jalali.Persian(day).gregorian_datetime()
        except Exception:
            None

        start_week = date - datetime.timedelta((date.weekday() + 2) % 7)
        end_week = start_week + datetime.timedelta(6)
        if week is None:
            return Reservation.objects.filter(doctor=self.request.user.system_user.role.office.doctor, date=date)
        return Reservation.objects.filter(doctor=self.request.user.system_user.role.office.doctor,
                                          date__range=[start_week, end_week])
