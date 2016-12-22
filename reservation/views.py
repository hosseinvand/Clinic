from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.urls.base import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.views.generic.edit import FormView
from reservation.forms import SystemUserRegisterForm, DoctorRegisterForm
from reservation.models import SystemUser, Doctor
from .forms import LoginForm


class MainPageView(TemplateView):
    template_name = 'home_page.html'


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


class DoctorCreateView(CreateView):
    model = Doctor
    template_name = 'doctor_register.html'
    success_url = reverse_lazy('mainPage')
    form_class = DoctorRegisterForm

    #overriden just for logging request user
    def get(self, request, *args, **kwargs):
        print('get request to createview')
        print(request.user.is_authenticated())
        return super(CreateView, self).get(request, *args, **kwargs)