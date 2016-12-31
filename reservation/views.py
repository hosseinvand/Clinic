from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.test.runner import filter_tests_by_tags
from django.urls.base import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
import sys

from reservation.forms import *
from .forms import LoginForm
from reservation.models import Secretary, Patient, PATIENT_ROLE_ID
from reservation.tests.mixins import PatientRequiredMixin, DoctorRequiredMixin


class MainPageView(TemplateView, FormView):
    template_name = 'home_page.html'

    form_class = DoctorSearchForm

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        print(context.keys())
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
        SystemUser.objects.filter(user=user).update(role=Patient.load())
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
        # filter by name
        name = self.request.GET.get('name', '')
        print('name: ', name, " ")
        if name:
            words = name.split()
            for word in words:
                tmp_list = self.object_list.filter(user_role__user__first_name__icontains=word) | self.object_list.filter(
                    user_role__user__last_name__icontains=word)
                self.object_list = list(set(self.object_list)&set(tmp_list))

        # filter by city
        city = self.request.GET.get('city', '')
        if city:
            self.object_list = self.object_list.filter(office__city__icontains=city)

        # filter by education
        edu = self.request.GET.get('education', '')
        if edu:
            self.object_list = self.object_list.filter(education__icontains=edu)

        # filter by speciality
        spec = self.request.GET.get('speciality', '')
        if spec:
            self.object_list = self.object_list.filter(speciality__icontains=spec)

        # filter by max price
        max_price = self.request.GET.get('max_price', '')
        if max_price:
            self.object_list = self.object_list.filter(price__lte=max_price)

        # filter by insurance
        ins = self.request.GET.get('insurance', '')
        if ins:
            self.object_list = self.object_list.filter(insurance__icontains=ins)

        # filter by opening time
        from_h = self.request.GET.get('from_hour', '')
        to_h = self.request.GET.get('to_hour', '')
        if from_h:
            self.object_list = self.object_list.filter(office__to_hour__gte=from_h)
        if to_h:
            self.object_list = self.object_list.filter(office__from_hour__lte=to_h)

        return self.object_list

class SecretaryPanel(LoginRequiredMixin, TemplateView):
    selected = "panel"
    template_name = 'panel.html'


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
            print("cannn")
            office = request.user.system_user.role.office
            secretary_role = Secretary(office=office)
            secretary_role.save()
            secretary_user.role = secretary_role
            secretary_user.save()
        return redirect(reverse_lazy("ManageSecretary"))

    def entered_username_can_become_secretary(self, secretary_user):
        print(secretary_user.role.get_role_id())
        return secretary_user.role.get_role_id() == PATIENT_ROLE_ID


@login_required
def deleteSecretary(request):
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


class AddClinicView(LoginRequiredMixin, CreateView):
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

    def get_object(self):
        return SystemUser.objects.get(user=self.request.user).role.office


class DoctorProfileView(DetailView):
    model = Doctor
    template_name = 'doctor_profile.html'

