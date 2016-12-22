from django.conf.urls import url
from django.contrib.auth.views import logout

from reservation.views import *

__author__ = 'mohre'

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='mainPage'),
    url(r'^login/$', SystemUserLoginView.as_view(), name="login"),
    url(r'^logout/$', logout, {'next_page': reverse_lazy('mainPage')}),
    url(r'^register/$', SystemUserCreateView.as_view(), name='register'),
    url(r'^register/doctor$', DoctorCreateView.as_view(), name='doctorRegister'),
    url(r'^search/(?P<searched>.*)/$', SearchDoctorView.as_view(), name='searchResult'),


    url(r'^panel/$', SecretaryPanel.as_view(), name="panel"),
    url(r'^secretary/$', ManageSecretary.as_view(), name="ManageSecretary"),
    url(r'^clinic/$', AddClinicView.as_view(), name="addClinic"),
    url(r'^clinic/(?P<pk>\d+)$', UpdateClinicView.as_view(), name="updateClinic"),
]
