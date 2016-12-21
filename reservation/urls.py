from django.conf.urls import url
from django.contrib.auth.views import logout
from django.urls.base import reverse_lazy

from reservation.views import MainPageView, SystemUserCreateView, SystemUserLoginView

__author__ = 'mohre'

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='mainPage'),
    url(r'^login/$', SystemUserLoginView.as_view(), name="login"),
    url(r'^logout/$', logout, {'next_page': reverse_lazy('mainPage')}),
    url(r'^register/$', SystemUserCreateView.as_view(), name='register'),

]