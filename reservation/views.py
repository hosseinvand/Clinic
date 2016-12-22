from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls.base import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from reservation.forms import SystemUserRegisterForm, DoctorRegisterForm
from reservation.models import SystemUser, Doctor
from .forms import LoginForm


class MainPageView(TemplateView):
    template_name = 'home_page.html'
    # form_class = DoctorSearchForm


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


class DoctorCreateView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'     #TODO: doesnt work..
    model = Doctor
    template_name = 'doctor_register.html'
    success_url = reverse_lazy('mainPage')
    form_class = DoctorRegisterForm




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
