"""
WSGI config for Clinic project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise
from Clinic import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Clinic.settings")

application = get_wsgi_application()
if settings.HEROKU:
    application = DjangoWhiteNoise(application)
