from django.conf.urls import url
from django.contrib.auth.views import logout
from reservation.views import *

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='mainPage'),
    url(r'^login/$', SystemUserLoginView.as_view(), name='login'),
    url(r'^logout/$', logout, {'next_page': reverse_lazy('mainPage')}, name='logout'),
    url(r'^register/$', SystemUserCreateView.as_view(), name='register'),
    url(r'^register/doctor$', DoctorCreateView.as_view(), name='doctorRegister'),

    url(r'^search_results/$', SearchDoctorView.as_view(), name='searchResult'),
    url(r'^search_by_location/$', GetSearchByLocationOfficeResult.as_view(), name='searchLocation'),

    url(r'^panel/$', SecretaryPanel.as_view(), name="panel"),
    url(r'^panel/secretary/$', ManageSecretary.as_view(), name="ManageSecretary"),
    url(r'^ajax/delete_secretary/$', DeleteSecretary.as_view(), name='deleteSecretary'),
    url(r'^panel/clinic/$', AddClinicView.as_view(), name="addClinic"),
    url(r'^panel/clinic/edit$', UpdateClinicView.as_view(), name="updateClinic"),
    url(r'^panel/profile/$', UpdateSystemUserProfile.as_view(), name="systemUserProfile"),
    url(r'^panel/reservation/requests/$', ManageReservations.as_view(), name="manageReservations"),
    url(r'^panel/reservation/status/$', SecretaryPanel.as_view(), name="panel"),  # TODO: duplicate!
    url(r'^panel/reservation/list/$', ReservationListPanel.as_view(), name="reservationList"),

    url(r'^profile/(?P<pk>\d+)$', DoctorProfileView.as_view(), name="doctorProfile"),
    url(r'^reservation/(?P<pk>\d+)$', ReservationCreateView.as_view(), name="reservation"),
    url(r'^doctor_card/(?P<pk>\d+)$', GetDoctorCard.as_view(), name='doctorCard'),


    url(r'^ajax/reserve_time/$', ReserveTime.as_view(), name='reserveTime'),
    url(r'^ajax/reject_time/$', RejectRequestedTime.as_view(), name='rejectTime'),
    url(r'^ajax/search_by_location/$', GetSearchByLocationOfficeResult.as_view(), name='searchLocationOffice'),

]
