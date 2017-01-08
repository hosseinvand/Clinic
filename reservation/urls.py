from django.conf.urls import url
from django.contrib.auth.views import logout

from reservation import views
from reservation.views import *

__author__ = 'mohre'

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='mainPage'),
    url(r'^login/$', SystemUserLoginView.as_view(), name='login'),
    url(r'^logout/$', logout, {'next_page': reverse_lazy('mainPage')}, name='logout'),
    url(r'^register/$', SystemUserCreateView.as_view(), name='register'),
    url(r'^register/doctor$', DoctorCreateView.as_view(), name='doctorRegister'),
    # url(r'^search/(?P<searched>.*)/$', SearchDoctorView.as_view(), name='searchResult'),

    url(r'^search_results/$', SearchDoctorView.as_view(), name='searchResult'),

    url(r'^panel/$', SecretaryPanel.as_view(), name="panel"),
    url(r'^panel/secretary/$', ManageSecretary.as_view(), name="ManageSecretary"),
    url(r'^ajax/delete_secretary/$', views.deleteSecretary, name='deleteSecretary'),
    url(r'^panel/clinic/$', AddClinicView.as_view(), name="addClinic"),
    url(r'^panel/clinic/edit$', UpdateClinicView.as_view(), name="updateClinic"),
    url(r'^panel/search$', PanelSearch.as_view(), name="panelSearch"),
    url(r'^panel/profile/$', UpdateSystemUserProfile.as_view(), name="systemUserProfile"),
    url(r'^panel/reservation/requests/$', ManageReservations.as_view(), name="manageReservations"),
    url(r'^panel/reservation/status/$', SecretaryPanel.as_view(), name="panel"),#TODO: duplicate!

    url(r'^profile/(?P<pk>\d+)$', DoctorProfileView.as_view(), name="doctorProfile"),
    url(r'^reservation/(?P<pk>\d+)$', ReservationCreateView.as_view(), name="reservation"),


    url(r'^ajax/reserve_time/$', views.reserveTime, name='deleteSecretary'),

]
