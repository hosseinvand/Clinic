from django.conf.urls import url

from notebook.views import MainPageView, Login, DoctorsView

urlpatterns = [
    url(r'^api/login/$', Login.as_view(), name='react_login'),
    url(r'^api/doctors/$', DoctorsView.as_view(), name='react_doctors'),
    url(r'^$', MainPageView.as_view(), name='react_home'),
    url(r'^(?:.*)/?$', MainPageView.as_view()),
]