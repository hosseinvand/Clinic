from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy
from reservation.models import SystemUser, DOCTOR_ROLE_ID, PATIENT_ROLE_ID, SECRETARY_ROLE_ID

__author__ = 'mohre'


class PatientRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        role = SystemUser.objects.get(user=request.user).role
        if not role.get_role_id() == PATIENT_ROLE_ID:
            return HttpResponseRedirect(reverse_lazy('panel'))
        return super(PatientRequiredMixin, self).dispatch(request, *args, **kwargs)


class DoctorRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        role = SystemUser.objects.get(user=request.user).role
        if not role.get_role_id() == DOCTOR_ROLE_ID:
            return HttpResponseRedirect(reverse_lazy('panel'))
        return super(DoctorRequiredMixin, self).dispatch(request, *args, **kwargs)


class SecretaryRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        role = SystemUser.objects.get(user=request.user).role
        if not role.get_role_id() == SECRETARY_ROLE_ID:
            return HttpResponseRedirect(reverse_lazy('panel'))
        return super(SecretaryRequiredMixin, self).dispatch(request, *args, **kwargs)

