from django.conf.urls import url
from django.contrib.auth.views import logout
from django.urls import reverse_lazy

from notebook.views import MainPageView, Login, DoctorsView, DoctorDetailView, ReservationsView

urlpatterns = [
    url(r'^logout/$', logout, {'next_page': "/notebook/login"}, name='react_logout'),
    url(r'^api/login/$', Login.as_view(), name='react_login'),
    url(r'^api/doctors/$', DoctorsView.as_view(), name='react_doctors'),
    url(r'^api/reservations/$', ReservationsView.as_view(), name='react_reservations'),
    url(r'^api/doctor/(?P<pk>\d+)/$', DoctorDetailView.as_view(), name='react_doctor_detail'),
    url(r'^$', MainPageView.as_view(), name='react_home'),
    url(r'^(?:.*)/?$', MainPageView.as_view()),
]