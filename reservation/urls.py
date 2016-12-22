from django.conf.urls import url
from django.contrib.auth.views import logout

from reservation.views import *

__author__ = 'mohre'

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='mainPage'),
    url(r'^panel/$', SecretaryPanel.as_view(), name="panel"),
    url(r'^login/$', SystemUserLoginView.as_view(), name="login"),
    url(r'^logout/$', logout, {'next_page': reverse_lazy('mainPage')}),
    url(r'^register/$', SystemUserCreateView.as_view(), name='register'),
    url(r'^register/doctor$', DoctorCreateView.as_view(), name='doctorRegister'),

]