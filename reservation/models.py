from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    user = models.OneToOneField(User, related_name="patient_user")
#     role = models.OneToOneField(Role, related_name='patient_role')
#
#
# class Role:
#     None
