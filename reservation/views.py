from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from reservation.forms import PatientRegisterForm
from reservation.models import Patient


class MainPageView(TemplateView):
    template_name = 'home_page.html'

class PatientCreateView(CreateView):
    model = Patient
    template_name = 'signup.html'
    # success_url = reverse_lazy('home')
    form_class = PatientRegisterForm