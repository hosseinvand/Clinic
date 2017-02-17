from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from django.views.generic import TemplateView


class MainPageView(TemplateView):
    template_name = 'react_home.html'


class Login(View):
    # def dispatch(self, request, *args, **kwargs):
    #     print("hhshdhdshsshhd")
    #     return super(Login, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(request.body)
        username, password = request.body.get('username'), request.POST.get('password')
        print(username, password)
        try:
            user = authenticate(username=username, password=password)
            login(self.request, user)
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=401)
