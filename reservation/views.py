from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.urls.base import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.views.generic.edit import FormView
from reservation.forms import PatientRegisterForm
from reservation.models import Patient
from .forms import LoginForm


class MainPageView(TemplateView):
    template_name = 'home_page.html'


class PatientCreateView(CreateView):
    model = Patient
    template_name = 'signup.html'
    success_url = reverse_lazy('mainPage')
    form_class = PatientRegisterForm

    def form_valid(self, form):
        response = super(PatientCreateView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return response


class PatientLoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('mainPage')

    def form_valid(self, form):
        response = super(PatientLoginView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response

    def get_context_data(self, **kwargs):
        context = super(PatientLoginView, self).get_context_data(**kwargs)
        context['submit_button'] = 'Login'
        return context
