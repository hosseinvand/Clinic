from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
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
    # success_url = reverse_lazy('home')
    success_url = '/'
    form_class = PatientRegisterForm

    def form_valid(self, form):
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return super(PatientCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PatientCreateView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class PatientLoginView(FormView):
    template_name = 'signup.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        user = User.objects.get(username=form.cleaned_data['username'])
        login(self.request, user)
        return super(PatientLoginView, self).form_valid(form)
