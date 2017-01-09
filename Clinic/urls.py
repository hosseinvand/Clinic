
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static

from Clinic import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('reservation.urls')),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
# else:
urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
