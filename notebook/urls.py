from django.conf.urls import url

from notebook.views import MainPageView

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='mainPage'),
]