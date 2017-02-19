import datetime
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls.base import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from reservation import models
from reservation.forms import *
from reservation.minheap import Heap
from reservation.mixins import PatientRequiredMixin, DoctorRequiredMixin, DoctorSecretaryRequiredMixin
from reservation.models import Secretary, Patient, PATIENT_ROLE_ID
from .forms import LoginForm


class MainPageView(TemplateView, FormView):
    template_name = 'home_page.html'

    form_class = DoctorSearchForm

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        return context


class SystemUserCreateView(CreateView):
    model = SystemUser
    template_name = 'signup.html'
    success_url = reverse_lazy('mainPage')
    form_class = SystemUserRegisterForm

    def form_valid(self, form):
        response = super(SystemUserCreateView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password')
        new_user = authenticate(username=username, password=password)
        user = User.objects.get(username=username)
        role = Patient()
        role.save()
        SystemUser.objects.filter(user=user).update(role=role)
        login(self.request, new_user)
        return response


class SystemUserLoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('mainPage')

    def form_valid(self, form):
        response = super(SystemUserLoginView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response

    def get_context_data(self, **kwargs):
        context = super(SystemUserLoginView, self).get_context_data(**kwargs)
        context['submit_button'] = 'Login'
        return context


class DoctorCreateView(LoginRequiredMixin, PatientRequiredMixin, CreateView):
    model = Doctor
    template_name = 'doctor_register.html'
    success_url = reverse_lazy('mainPage')
    form_class = DoctorRegisterForm

    def form_valid(self, form):
        print('form is valid')
        response = super(DoctorCreateView, self).form_valid(form)
        doctor = Doctor.objects.get(doctor_code=form.cleaned_data['doctor_code'])
        SystemUser.objects.filter(user=self.request.user).update(role=doctor)
        return response


class SearchDoctorView(ListView, FormView):
    model = Doctor
    template_name = 'search_results.html'
    form_class = DoctorSearchForm

    def __init__(self):
        super(SearchDoctorView, self).__init__()
        self.object_list = None

    def get_initial(self):
        initial = super(SearchDoctorView, self).get_initial()
        field_list = self.request.GET
        for field in field_list:
            initial[field] = self.request.GET.get(field, '')
        return initial

    def get_queryset(self):
        self.object_list = self.model.objects.all()
        print("object list: ", self.object_list)
        print("params: ", self.request.GET)
        # filter by name
        name = self.request.GET.get('name', '')
        if name:
            words = name.split()
            print('words: ', words)
            for word in words:
                self.object_list = self.object_list.filter(
                    user_role__user__first_name__icontains=word) | self.object_list.filter(
                    user_role__user__last_name__icontains=word)

        # filter by city
        city = self.request.GET.get('city', '')
        if city:
            self.object_list = self.object_list.filter(office__city__iexact=city)

        # filter by education
        edu = self.request.GET.get('education', '')
        if edu:
            self.object_list = self.object_list.filter(education__iexact=edu)

        # filter by speciality
        spec = self.request.GET.get('speciality', '')
        if spec:
            self.object_list = self.object_list.filter(speciality__iexact=spec)

        # filter by max price
        max_price = self.request.GET.get('max_price', '')
        if max_price:
            max_price = int(max_price)
            self.object_list = self.object_list.filter(price__lte=max_price)

        # filter by insurance
        ins = self.request.GET.get('insurance', '')
        if ins:
            self.object_list = self.object_list.filter(insurance__iexact=ins)

        # filter by opening time
        from_h = self.request.GET.get('from_hour', '')
        to_h = self.request.GET.get('to_hour', '')
        if from_h:
            from_h = int(from_h)
            self.object_list = self.object_list.filter(office__to_hour__gt=from_h)
        if to_h:
            to_h = int(to_h)
            self.object_list = self.object_list.filter(office__from_hour__lt=to_h)

        return self.object_list


class GetDoctorCard(TemplateView):
    template_name = 'doctor_card.html'

    def get_context_data(self, **kwargs):
        context = super(GetDoctorCard, self).get_context_data(**kwargs)
        context['doctor'] = models.Doctor.objects.filter(pk=kwargs['pk']).first()
        return context


class GetSearchByLocationOfficeResult(ListView):
    model = Doctor
    template_name = 'search_by_location.html'

    def __init__(self):
        super(GetSearchByLocationOfficeResult, self).__init__()
        self.object_list = None
        self.office_id_list = None

    def post(self, request, *args, **kwargs):
        all_offices = models.Office.objects.all()
        count = 20  # TODO: input from user

        # sorted by distance id list
        office_id_list = self.get_list_of_top_office_ids(all_offices, float(request.POST.get('lat')),
                                                         float(request.POST.get('lng')), count)

        print("top offices: ", office_id_list)
        # not sorted by distance
        offices_values = models.Office.objects.filter(id__in=office_id_list).values('lat_position', 'lng_position',
                                                                                    'doctorSecretary')

        return JsonResponse(list(offices_values), safe=False)

    # put offices in heap to find nearest ones
    def get_list_of_top_office_ids(self, offices, loc_lat, loc_lng, number):
        office_id_list = []
        inf_dist = 100000
        max_heap = Heap()
        for office in offices:
            dist = office.distance(loc_lat, loc_lng)
            max_heap.push(inf_dist - dist, office.id)
            if len(max_heap) > number:
                max_heap.pop()

        while len(max_heap) > 0:
            office_id_list.append(max_heap.pop())

        office_id_list.reverse()
        self.office_id_list = office_id_list
        return office_id_list


class ManageSecretary(LoginRequiredMixin, ListView):
    selected = "manageSecretary"
    model = Secretary
    template_name = 'panel.html'

    def get_queryset(self):
        object_list = self.model.objects.filter(office=self.request.user.system_user.role.office)
        return object_list

    def getSystemUserByUsername(self, username):
        try:
            return User.objects.get(username=username).system_user
        except User.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        secretary_username = request.POST.get('username')
        secretary_user = self.getSystemUserByUsername(secretary_username)

        if not secretary_user:
            return HttpResponse("خطا! منشی وجود ندارد.")

        if self.entered_username_can_become_secretary(secretary_user):
            office = request.user.system_user.role.office
            secretary_role = Secretary(office=office)
            secretary_role.save()
            secretary_user.role = secretary_role
            secretary_user.save()
        return redirect(reverse_lazy("ManageSecretary"))

    def entered_username_can_become_secretary(self, secretary_user):
        return secretary_user.role.get_role_id() == PATIENT_ROLE_ID


@login_required
def delete_secretary(request):
    # office = request.user.system_user.role.office
    # TODO don't allow user to delete secretary of other doctors
    username = request.POST.get('username', None)
    user = User.objects.get(username=username).system_user
    user.role.delete()
    patient_role = Patient()
    patient_role.save()
    user.role = patient_role
    user.save()
    return JsonResponse({})


@login_required
def reserve_time(request):
    reservation_pk = request.POST.get('reservationPk', None)
    range_num = request.POST.get('rangeNum', None)
    Reservation.objects.filter(pk=reservation_pk).update(range_num=range_num)
    return JsonResponse({})


@login_required
def reject_time(request):
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


class PanelSearch(LoginRequiredMixin, TemplateView):
    selected = "panelSearch"
    template_name = 'panel.html'


class UpdateClinicView(LoginRequiredMixin, DoctorRequiredMixin, UpdateView):
    selected = "updateClinic"
    model = Office
    template_name = 'panel.html'
    success_url = reverse_lazy('panel')
    form_class = ClinicForm

    def get_object(self, queryset=None):
        x = SystemUser.objects.get(user=self.request.user).role.office
        print(x.get_available_days())
        return x


class UpdateSystemUserProfile(LoginRequiredMixin, UpdateView):
    selected = "updateProfile"
    model = User
    template_name = 'panel.html'
    success_url = reverse_lazy('panel')
    form_class = SystemUserUpdateForm

    def get_object(self, queryset=None):
        return SystemUser.objects.get(user=self.request.user).user

    def get_form_kwargs(self):
        kwargs = super(UpdateSystemUserProfile, self).get_form_kwargs()
        kwargs.update({'initial': {'id_code': self.request.user.system_user.id_code}})
        return kwargs


class ManageReservations(LoginRequiredMixin, DoctorSecretaryRequiredMixin, ListView):
    selected = "reservation"
    template_name = 'panel.html'

    def get_queryset(self):
        return Reservation.objects.filter(range_num__isnull=True,
                                          doctor=self.request.user.system_user.role.office.doctor)


class DoctorProfileView(DetailView):
    model = Doctor
    template_name = 'doctor_profile.html'


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    template_name = 'reservation.html'
    form_class = ReservationDateTimeForm
    success_url = reverse_lazy("panel")

    def get_context_data(self, **kwargs):
        context = super(ReservationCreateView, self).get_context_data(**kwargs)
        context['doctor'] = Doctor.objects.get(pk=self.kwargs['pk'])
        context['patient'] = self.request.user.system_user
        return context


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
