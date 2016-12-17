from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from Clinic import settings
from reservation.views import MainPageView, PatientCreateView

__author__ = 'mohre'

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='mainPage'),
    url(r'^register/$', PatientCreateView.as_view(), name='registerPage'),

]