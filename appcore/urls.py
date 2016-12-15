from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from Clinic import settings
from appcore.views import MainPageView

__author__ = 'mohre'

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='mainPage'),
]