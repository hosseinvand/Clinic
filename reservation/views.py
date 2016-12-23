from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from reservation.forms import *
from .forms import LoginForm


class MainPageView(TemplateView):
    template_name = 'home_page.html'
    # form_class = DoctorSearchForm

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
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


class DoctorCreateView(LoginRequiredMixin, CreateView):
    model = Doctor
    template_name = 'doctor_register.html'
    success_url = reverse_lazy('mainPage')
    form_class = DoctorRegisterForm

    def form_valid(self, form):
        print('form is valid')
        response = super(CreateView, self).form_valid(form)
        doctor = Doctor.objects.get(doctor_code=form.cleaned_data['doctor_code'])
        SystemUser.objects.filter(user=self.request.user).update(role=doctor)
        return response

class SearchDoctorView(ListView):
    model = SystemUser
    template_name = 'search_results.html' #TODO

    # def get_queryset(self):
    #     text = self.kwargs.get('searched')
    #     ans = self.model.objects.filter(type__icontains=text) | self.model.objects.filter(name__icontains=text)
    #     return ans

    def get_queryset(self):
        name = self.kwargs.get('searched')
        print('name: ', name, " ")

        if name is not None:
            object_list = self.model.objects.all()
            #TODO: return doctors which their name is 'name'
            # user = User.objects.filter(first_name=name)
            # object_list = self.model.objects.filter(user__icontains=user)
        else:
            object_list = self.model.objects.all()
        return object_list



class SecretaryPanel(LoginRequiredMixin, TemplateView):
    selected = "panel"
    template_name = 'panel.html'


class ManageSecretary(LoginRequiredMixin, TemplateView):
    selected = "manageSecretary"
    template_name = 'panel.html'


class AddClinicView(LoginRequiredMixin, CreateView):
    selected = "addClinic"
    model = Office
    template_name = 'panel.html'
    success_url = reverse_lazy('mainPage')
    form_class = ClinicForm


class UpdateClinicView(LoginRequiredMixin, UpdateView):
    selected = "updateClinic"
    model = Office
    template_name = 'panel.html'
    form_class = ClinicForm
