from django.conf.urls import url

from notebook.views import MainPageView, Login

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='react_home'),
    url(r'^api/login/$', Login.as_view(), name='react_login'),
    url(r'^(?:.*)/?$', MainPageView.as_view()),
]