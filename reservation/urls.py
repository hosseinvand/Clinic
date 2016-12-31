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
    # url(r'^search/(?P<searched>.*)/$', SearchDoctorView.as_view(), name='searchResult'),

    url(r'^search_results/$', SearchDoctorView.as_view(), name='searchResult'),

    url(r'^panel/$', SecretaryPanel.as_view(), name="panel"),
    url(r'^panel/secretary/$', ManageSecretary.as_view(), name="ManageSecretary"),
    url(r'^panel/clinic/$', AddClinicView.as_view(), name="addClinic"),
    url(r'^panel/search$', PanelSearch.as_view(), name="panelSearch"),
    url(r'^clinic/(?P<pk>\d+)$', UpdateClinicView.as_view(), name="updateClinic"),
    url(r'^profile/(?P<pk>\d+)$', DoctorProfileView.as_view(), name="doctorProfile"),

]
